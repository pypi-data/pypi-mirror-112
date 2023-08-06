import { backfillMissingProvidersWithFallback, decideDefault, getUserDefaultValues, } from 'app/views/settings/account/notifications/utils';
describe('Notification Settings Utils', function () {
    describe('getUserDefaultValues', function () {
        describe('when notificationsSettings are empty', function () {
            it('should return fallback values', function () {
                expect(getUserDefaultValues('deploy', {})).toEqual({
                    email: 'committed_only',
                    slack: 'never',
                });
            });
        });
        describe('when notificationsSettings are not empty', function () {
            it('should return the parent-independent notificationSettings', function () {
                expect(getUserDefaultValues('alerts', {
                    alerts: {
                        user: {
                            me: {
                                email: 'never',
                                slack: 'never',
                            },
                        },
                    },
                })).toEqual({
                    email: 'never',
                    slack: 'never',
                });
            });
        });
    });
    describe('backfillMissingProvidersWithFallback', function () {
        describe('when scopeType is user', function () {
            it('should add missing provider with the fallback value', function () {
                expect(backfillMissingProvidersWithFallback({}, ['email'], 'sometimes', 'user')).toEqual({ email: 'sometimes', slack: 'never' });
            });
            it('should turn on both providers with the fallback value', function () {
                expect(backfillMissingProvidersWithFallback({ email: 'never', slack: 'never' }, ['email', 'slack'], 'sometimes', 'user')).toEqual({ email: 'sometimes', slack: 'sometimes' });
            });
            it('should move the existing setting when providers are swapped', function () {
                expect(backfillMissingProvidersWithFallback({ email: 'always', slack: 'never' }, ['slack'], '', 'user')).toEqual({ email: 'never', slack: 'always' });
            });
            it('should turn off both providers when providers is empty', function () {
                expect(backfillMissingProvidersWithFallback({ email: 'always', slack: 'always' }, [], '', 'user')).toEqual({ email: 'never', slack: 'never' });
            });
        });
    });
    describe('decideDefault', function () {
        describe('when there are no parent-specific settings', function () {
            describe('when the parent-independent settings match', function () {
                it('should return always when the settings are always', function () {
                    expect(decideDefault('alerts', {
                        alerts: {
                            user: {
                                me: {
                                    email: 'always',
                                    slack: 'always',
                                },
                            },
                        },
                    })).toEqual('always');
                });
                it('should return never when the settings are never', function () {
                    expect(decideDefault('alerts', {
                        alerts: {
                            user: {
                                me: {
                                    email: 'never',
                                    slack: 'never',
                                },
                            },
                        },
                    })).toEqual('never');
                });
            });
            describe('when the parent-independent settings do not match', function () {
                it('should return the always when the other value is never', function () {
                    expect(decideDefault('alerts', {
                        alerts: {
                            user: {
                                me: {
                                    email: 'always',
                                    slack: 'never',
                                },
                            },
                        },
                    })).toEqual('always');
                });
            });
        });
        describe('when there are parent-specific settings', function () {
            describe('when the parent-specific settings are "below" the parent-independent settings', function () {
                it('should "prioritize" always over never', function () {
                    expect(decideDefault('alerts', {
                        alerts: {
                            user: {
                                me: {
                                    email: 'never',
                                    slack: 'never',
                                },
                            },
                            project: {
                                1: {
                                    email: 'always',
                                    slack: 'always',
                                },
                            },
                        },
                    })).toEqual('always');
                });
                it('should "prioritize" sometimes over always', function () {
                    expect(decideDefault('alerts', {
                        alerts: {
                            user: {
                                me: {
                                    email: 'never',
                                    slack: 'never',
                                },
                            },
                            project: {
                                1: {
                                    email: 'subscribe_only',
                                    slack: 'subscribe_only',
                                },
                            },
                        },
                    })).toEqual('subscribe_only');
                });
            });
            describe('when the parent-specific settings are "above" the parent-independent settings', function () {
                it('should return the parent-specific settings', function () {
                    expect(decideDefault('alerts', {
                        alerts: {
                            user: {
                                me: {
                                    email: 'always',
                                    slack: 'always',
                                },
                            },
                            project: {
                                1: {
                                    email: 'never',
                                    slack: 'never',
                                },
                            },
                        },
                    })).toEqual('always');
                });
            });
        });
    });
});
//# sourceMappingURL=testUtils.spec.jsx.map