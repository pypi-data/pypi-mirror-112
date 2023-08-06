export var ALL_PROVIDERS = {
    email: 'default',
    slack: 'never',
};
/** These values are stolen from the DB. */
export var VALUE_MAPPING = {
    default: 0,
    never: 10,
    always: 20,
    subscribe_only: 30,
    committed_only: 40,
};
export var MIN_PROJECTS_FOR_SEARCH = 3;
export var MIN_PROJECTS_FOR_PAGINATION = 100;
export var NOTIFICATION_SETTINGS_TYPES = [
    'alerts',
    'deploy',
    'workflow',
    'reports',
    'email',
];
export var SELF_NOTIFICATION_SETTINGS_TYPES = [
    'personalActivityNotifications',
    'selfAssignOnResolve',
];
//# sourceMappingURL=constants.jsx.map