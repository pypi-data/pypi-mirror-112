/*
 * Trend App Protect libagent - core library for all agents.
 */

/** (python ignore start) **/
#ifndef _LIBAGENT_AGENT_H
#define _LIBAGENT_AGENT_H

#ifdef __cplusplus
extern "C" {
#endif
/** (python ignore end) **/

/*
 * Return values of `libagent_get_type`.
 */
#define LIBAGENT_TYPE_NIL       0
#define LIBAGENT_TYPE_BOOLEAN   1
#define LIBAGENT_TYPE_NUMBER    2
#define LIBAGENT_TYPE_STRING    3
#define LIBAGENT_TYPE_TABLE     4
#define LIBAGENT_TYPE_FUNCTION  5

/*
 * Log levels.
 */
#define LIBAGENT_LOG_ERROR      1
#define LIBAGENT_LOG_WARN       2
#define LIBAGENT_LOG_INFO       3
#define LIBAGENT_LOG_DEBUG      4
#define LIBAGENT_LOG_TRACE      5

/*
 * `libagent_version` returns the current version of libagent.
 *
 * Drop the returned string using `libagent_drop_string`.
 */
const char *libagent_version();

/*
 * `libagent_Config` holds the agent configuration.
 *
 * When passed to `libagent_new_agent`, configuration from `LIBAGENT_*` env vars
 * will be loaded and take precedence over the values set in this config.
 */
typedef struct libagent_Config libagent_Config;
libagent_Config *libagent_new_config();

/*
 * Set the value of a config. The value must be passed as a string. It will be
 * parsed to the proper type internally (see src/config/parse.rs).
 *
 * See src/config/defaults.rs for the full list of configuration and their
 * default values.
 *
 * On success, `1` is returned.
 * On error, `0` is returned and the error is logged to the location specified
 * in the "log_file" config.
 */
int libagent_set_config(libagent_Config *config, const char *field, const char *value);

/*
 * `libagent_Agent` is the entry point to the lib.
 */
typedef struct libagent_Agent libagent_Agent;

/*
 * Creates a new agent. Several agents can co-exist, each with their own config and transactions.
 *
 * `type`: provides the `agent_type` to the backend, such as `agent-ruby`.
 * `version`: provides the `agent_version` to the backend, and must be the version of the host
 * language agent, NOT the version of libagent.
 * `config`: must be created using `libagent_new_config`.
 *
 * If the agent is disabled (config.agent_enabled = false) a mock agent is returned. A mock agent
 * will silently ignore all calls bellow but libagent_log*. However, libagent_start_transaction will
 * return NULL. You are responsible for handling this special case.
 *
 * If the operation fails, the error is logged to config.log_file, and a mock agent is returned.
 *
 * The `libagent_Config` will be dropped by this function. Do not call `libagent_set_config` on
 * it afterwards.
 */
libagent_Agent *libagent_new_agent(const char *type, const char *version, libagent_Config *config);

/*
 * Returns `1` if the agent is enabled. `0` if the agent is disabled because of configuration or
 * an error during initialization.
 */
int libagent_is_enabled(libagent_Agent *agent);

/*
 * Returns `1` if the agent is in DEBUG_MODE (debug_mode=true config).
 * `0` if not.
 */
int libagent_is_debug_mode(libagent_Agent *agent);

/*
 * Close and drop the agent from memory.
 *
 * Optional.
 */
void libagent_close_agent(libagent_Agent *agent);

/*
 * Schedule a bit of environment information to be reported to the back-end.
 *
 * `type`: One of "runtime" or "language".
 * `name`: is required.
 * `version`: can be NULL.
 *
 * On success, `1` is returned.
 * On error, `0` is returned and the error is logged.
 */
int libagent_report(libagent_Agent *agent, const char *type,
                                           const char *name,
                                           const char *version);

/*
 * Schedule a plugin status to be reported to the back-end.
 *
 * `name`: is required and must be unique to report a new plugin or else,
 * it will perform an update on the information from the previous call.
 * `hooks`: is a comma-separated list or hooks provided by the plugin,
 * or NULL to leave unchanged from previous call.
 * `status`: is one of: "pending", "loaded", "failed", "disabled",
 * or NULL to leave unchanged from previous call.
 * `version`: can be NULL to leave unchanged from previous call.
 *
 * Typically, on startup, you'd register each plugins with:
 *
 *     libagent_report_plugin(agent, "my_plugin", "hook1, hook2", "pending", NULL);
 *
 * Then, when the plugin is loaded:
 *
 *     libagent_report_plugin(agent, "my_plugin", NULL, "loaded", "1.0.0");
 *
 * On success, `1` is returned.
 * On error, `0` is returned and the error is logged.
 */

int libagent_report_plugin(libagent_Agent *agent,
                           const char *name,
                           const char *hooks,
                           const char *status,
                           const char *version);


/*
 * Returns `true` if the `plugin` enabled according to the agent config.
 */
int libagent_is_plugin_enabled(libagent_Agent *agent, const char *plugin);


/*
 * Send a message to the back-end Agent Manager.
 *
 * On success, `1` is returned.
 * On error, `0` is returned and the error is logged.
 */
int libagent_send_message(libagent_Agent *agent,
                          const char *type,
                          const char *version,
                          const char *mimetype,
                          const char *encoding,
                          const char *payload_bytes,
                          size_t payload_len);

/*
 * `libagent_Transaction` usually represents an HTTP request-response transaction. But could also
 * represent any other type of transaction. It holds all the information relative to that one
 * transaction.
 *
 * WARNING: An `libagent_Transaction` is NOT thread-safe. It should be stored in a thread-local
 * variable and should NOT be shared between threads.
 */
typedef struct libagent_Transaction libagent_Transaction;

/*
 * Starts a transaction.
 *
 * Pass `NULL` as uuid to have it automatically generated.
 *
 * WARNING: If the agent is disabled, this will return NULL.
 */
libagent_Transaction *libagent_start_transaction(libagent_Agent *agent, const char *uuid);

/*
 * Terminate the transaction, send the data to the back-end (if appropriate) and
 * drop it.
 */
void libagent_finish_transaction(libagent_Transaction *transaction);

/*
 * Returns the unique identifier of this transaction.
 */
const char *libagent_transaction_uuid(libagent_Transaction *transaction);

/*
 * A table can represent an array (1-based index) or a map.
 * They are used for passing arguments and as the return value when running
 * hooks (see `libagent_run_hook`).
 *
 * They are internally represented as a Lua table.
 *
 * See https://www.lua.org/pil/2.5.html.
 */
typedef struct libagent_Table libagent_Table;

/*
 * Create an array-like Lua table.
 *
 * NOTE: Arrays use 1-based index in Lua.
 */
libagent_Table *libagent_create_array(libagent_Transaction *transaction, size_t array_size);

/*
 * Create a map-like Lua table.
 *
 * Sets `__is_dict` in the metadata.
 */
libagent_Table *libagent_create_map(libagent_Transaction *transaction, size_t map_size);

/*
 * Drop (free) a table from memory.
 *
 * ALL returned or created tables must be freed with this function,
 * or else, it will leak.
 */
void libagent_drop_table(libagent_Table *table);

/*
 * Drop (free) a string returned by one of the `libagent_` functions.
 *
 * WARNING: Only drop a string that was RETURNED by an `libagent_` function.
 */
void libagent_drop_string(const char *str);

/*
 * Set a value in a map-like table at a string key.
 *
 * `libagent_set_string` must pass the string length (without the final NULL byte).
 */
void libagent_set_nil(libagent_Table *table, const char *key);
void libagent_set_boolean(libagent_Table *table, const char *key, int value);
void libagent_set_number(libagent_Table *table, const char *key, double value);
void libagent_set_table(libagent_Table *table, const char *key, libagent_Table *value);
void libagent_set_string(libagent_Table *table, const char *key,
                         const char *value, size_t len);

/*
 * Set a value in an array-like table at an index.
 *
 * `libagent_seti_string` must pass the string length (without the final NULL byte).
 */
void libagent_seti_nil(libagent_Table *table, int index);
void libagent_seti_boolean(libagent_Table *table, int index, int value);
void libagent_seti_number(libagent_Table *table, int index, double value);
void libagent_seti_table(libagent_Table *table, int index, libagent_Table *value);
void libagent_seti_string(libagent_Table *table, int index,
                          const char *value, size_t len);

/*
 * Returns the length of an array-like table.
 *
 * Does not return the number of entries in a map-like table.
 *
 * See https://www.lua.org/manual/5.1/manual.html#2.5.5
 */
size_t libagent_len(libagent_Table *table);

/*
 * Get the type of a value at key or index.
 * 
 * See LIBAGENT_TYPE_* at the top.
 */
int libagent_get_type(libagent_Table *table, const char *key);
int libagent_geti_type(libagent_Table *table, int index);

/*
 * Get the value from a map-like table entry.
 *
 * `libagent_get_boolean` returns false if the value is not a boolean.
 * `libagent_get_number` returns 0.0 if the value is not a number.
 * `libagent_get_table` and `libagent_get_string return NULL if the value is not
 *  the requested type.
 *
 * If a string can contain null bytes, use `libagent_get_bytes`.
 * `libagent_get_string` will return NULL if it contains a null byte.
 *
 * Drop the returned table or string using their respective `libagent_drop_*`.
 */
int libagent_get_boolean(libagent_Table *table, const char *key);
double libagent_get_number(libagent_Table *table, const char *key);
libagent_Table *libagent_get_table(libagent_Table *table, const char *key);
const char *libagent_get_string(libagent_Table *table, const char *key);
const char *libagent_get_bytes(libagent_Table *table, const char *key, size_t *len);

/*
 * Get the value from a array-like table entry.
 *
 * See note above in `libagent_get_` about fall-back values and strings.
 *
 * Drop the returned table or string using their respective `libagent_drop_*`.
 */
int libagent_geti_boolean(libagent_Table *table, int index);
double libagent_geti_number(libagent_Table *table, int index);
libagent_Table *libagent_geti_table(libagent_Table *table, int index);
const char *libagent_geti_string(libagent_Table *table, int index);
const char *libagent_geti_bytes(libagent_Table *table, int index, size_t *len);


/*
 * Returns the content of the table as a string. Useful for debugging.
 *
 * Drop the returned string using `libagent_drop_string`.
 */
const char *libagent_debug(libagent_Table *table);

/*
 * Append a log message using the agent logger.
 */
void libagent_log(
  libagent_Agent *agent,
  const char *target,
  const char *file,
  int line,
  int level,
  const char *message);

/*
 * Returns `true` if the agent logger currently logs at this level.
 * Useful if you want to log something that is expensive to convert to a string.
 */
int libagent_is_log_enabled(libagent_Agent *agent, int level);


/*
 * Time the execution of a block of code.
 *
 * Only plugin hook code should be timed for now. Hook execution is already
 * timed internally.
 *
 * `libagent_new_timer` will return `NULL` if timing is disabled.
 *
 * The timings will be reported to the channel after the transaction finishes,
 * and will be logged if the log_timings config is true.
 *
 * Ensure `libagent_start_timer` is called to initially start the timer.
 * `libagent_start_timer` and `libagent_stop_timer` can be called multiple times.
 * Ensure `libagent_finish_timer` is always called or else the timer will leak.
 */
typedef struct libagent_Timer libagent_Timer;

libagent_Timer *libagent_new_timer(libagent_Transaction *transaction,
                                   const char *kind,
                                   const char *name);
void libagent_start_timer(libagent_Timer *timer);
void libagent_stop_timer(libagent_Timer *timer);
void libagent_finish_timer(libagent_Timer *timer,
                          libagent_Transaction *transaction);

/*
 * Run a hook for a given transaction.
 *
 * `meta` can be NULL if none.
 *
 * On success, it will return a table. You are responsible for dropping that
 * table using `libagent_drop_table`.
 *
 * On error or if transaction was `NULL`, it will return `NULL`.
 */
libagent_Table *libagent_run_hook(libagent_Transaction *transaction,
                                  const char *plugin, const char *hook,
                                  libagent_Table *meta);

/*
 * Returns `true` if the `hook` can be run in this transaction.
 */
int libagent_has_hook(libagent_Transaction *transaction, const char *hook);

/*
 * Returns `true` if the `hook` already ran for this transaction.
 */
int libagent_hook_ran(libagent_Transaction *transaction, const char *hook);

/** (python ignore start) **/
#ifdef __cplusplus
}
#endif

#endif
/** (python ignore end) **/