function app() {
    return __awaiter(this, void 0, void 0, function () {
        var _a, bootstrap, initializeMain, data;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, Promise.all([
                        import('app/bootstrap'),
                        import('app/bootstrap/initializeMain'),
                    ])];
                case 1:
                    _a = __read.apply(void 0, [_b.sent(), 2]), bootstrap = _a[0].bootstrap, initializeMain = _a[1].initializeMain;
                    return [4 /*yield*/, bootstrap()];
                case 2:
                    data = _b.sent();
                    initializeMain(data);
                    return [2 /*return*/];
            }
        });
    });
}
app();
//# sourceMappingURL=index.jsx.map