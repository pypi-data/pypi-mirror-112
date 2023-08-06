// check to see if a member has been disabled because of the member limit
export default function isMemberDisabledFromLimit(member) {
    var _a;
    return (_a = member === null || member === void 0 ? void 0 : member.flags['member-limit:restricted']) !== null && _a !== void 0 ? _a : false;
}
//# sourceMappingURL=isMemberDisabledFromLimit.jsx.map