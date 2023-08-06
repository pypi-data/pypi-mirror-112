import PropTypes from 'prop-types';
var Metadata = PropTypes.shape({
    value: PropTypes.string,
    message: PropTypes.string,
    directive: PropTypes.string,
    type: PropTypes.string,
    title: PropTypes.string,
    uri: PropTypes.string,
});
var Avatar = PropTypes.shape({
    avatarType: PropTypes.oneOf(['letter_avatar', 'upload', 'gravatar']),
    avatarUuid: PropTypes.string,
});
/**
 * A User is someone that has registered on Sentry
 */
var User = PropTypes.shape({
    avatar: Avatar,
    avatarUrl: PropTypes.string,
    dateJoined: PropTypes.string,
    email: PropTypes.string,
    emails: PropTypes.arrayOf(PropTypes.shape({
        is_verified: PropTypes.bool,
        id: PropTypes.string,
        email: PropTypes.string,
    })),
    has2fa: PropTypes.bool,
    hasPasswordAuth: PropTypes.bool,
    id: PropTypes.string,
    identities: PropTypes.array,
    isActive: PropTypes.bool,
    isManaged: PropTypes.bool,
    lastActive: PropTypes.string,
    lastLogin: PropTypes.string,
    username: PropTypes.string,
});
var EventOrGroupType = PropTypes.oneOf([
    'error',
    'csp',
    'hpkp',
    'expectct',
    'expectstaple',
    'default',
    'transaction',
]);
var Group = PropTypes.shape({
    id: PropTypes.string.isRequired,
    annotations: PropTypes.array,
    assignedTo: User,
    count: PropTypes.string,
    culprit: PropTypes.string,
    firstSeen: PropTypes.string,
    hasSeen: PropTypes.bool,
    isBookmarked: PropTypes.bool,
    isPublic: PropTypes.bool,
    isSubscribed: PropTypes.bool,
    lastSeen: PropTypes.string,
    level: PropTypes.string,
    logger: PropTypes.string,
    metadata: Metadata,
    numComments: PropTypes.number,
    permalink: PropTypes.string,
    project: PropTypes.shape({
        name: PropTypes.string,
        slug: PropTypes.string,
    }),
    shareId: PropTypes.string,
    shortId: PropTypes.string,
    status: PropTypes.string,
    statusDetails: PropTypes.object,
    title: PropTypes.string,
    type: EventOrGroupType,
    userCount: PropTypes.number,
});
var Team = PropTypes.shape({
    id: PropTypes.string.isRequired,
    slug: PropTypes.string.isRequired,
});
var Project = PropTypes.shape({
    // snuba returns id as number
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    slug: PropTypes.string.isRequired,
    // snuba results may not contain a `name` or `isBookmarked
    teams: PropTypes.arrayOf(Team),
    name: PropTypes.string,
    isBookmarked: PropTypes.bool,
    status: PropTypes.string,
});
var Organization = PropTypes.shape({
    id: PropTypes.string.isRequired,
});
export default {
    Group: Group,
    Organization: Organization,
    Project: Project,
    User: User,
};
//# sourceMappingURL=sentryTypes.jsx.map