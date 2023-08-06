import NotFound from 'app/components/errors/notFound';
import HookOrDefault from 'app/components/hookOrDefault';
// getsentry will add the view
var DisabledMemberComponent = HookOrDefault({
    hookName: 'component:disabled-member',
    defaultComponent: function () { return <NotFound />; },
});
export default DisabledMemberComponent;
//# sourceMappingURL=index.jsx.map