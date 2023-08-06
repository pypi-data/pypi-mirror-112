import { createContext } from 'react';
var SpanEntryContext = createContext({
    getViewChildTransactionTarget: function () { return undefined; },
});
export var Provider = SpanEntryContext.Provider;
export var Consumer = SpanEntryContext.Consumer;
//# sourceMappingURL=context.jsx.map