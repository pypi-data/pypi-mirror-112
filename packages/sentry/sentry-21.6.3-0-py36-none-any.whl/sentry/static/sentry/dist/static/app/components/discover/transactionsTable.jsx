import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import PanelTable from 'app/components/panels/panelTable';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { fieldAlignment, getAggregateAlias } from 'app/utils/discover/fields';
import { generateEventSlug } from 'app/utils/discover/urls';
import { getDuration } from 'app/utils/formatters';
import CellAction from 'app/views/eventsV2/table/cellAction';
import { GridCell, GridCellNumber } from 'app/views/performance/styles';
import { getTransactionComparisonUrl } from 'app/views/performance/utils';
var TransactionsTable = /** @class */ (function (_super) {
    __extends(TransactionsTable, _super);
    function TransactionsTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionsTable.prototype.getTitles = function () {
        var _a = this.props, eventView = _a.eventView, titles = _a.titles;
        return titles !== null && titles !== void 0 ? titles : eventView.getFields();
    };
    TransactionsTable.prototype.renderHeader = function () {
        var _a = this.props, tableData = _a.tableData, columnOrder = _a.columnOrder, baselineTransactionName = _a.baselineTransactionName;
        var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        var generateSortLink = function () { return undefined; };
        var tableTitles = this.getTitles();
        var headers = tableTitles.map(function (title, index) {
            var column = columnOrder[index];
            var align = fieldAlignment(column.name, column.type, tableMeta);
            if (column.key === 'span_ops_breakdown.relative') {
                return (<HeadCellContainer key={index}>
            <GuideAnchor target="span_op_relative_breakdowns">
              <SortLink align={align} title={title === t('operation duration') ? (<React.Fragment>
                      {title}
                      <StyledIconQuestion size="xs" position="top" title={t("Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once.")}/>
                    </React.Fragment>) : (title)} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </GuideAnchor>
          </HeadCellContainer>);
            }
            return (<HeadCellContainer key={index}>
          <SortLink align={align} title={title} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        });
        if (baselineTransactionName) {
            headers.push(<HeadCellContainer key="baseline">
          <SortLink align="right" title={t('Compared to Baseline')} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        }
        return headers;
    };
    TransactionsTable.prototype.renderRow = function (row, rowIndex, columnOrder, tableMeta) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, generateLink = _a.generateLink, baselineTransactionName = _a.baselineTransactionName, baselineData = _a.baselineData, handleBaselineClick = _a.handleBaselineClick, handleCellAction = _a.handleCellAction, titles = _a.titles;
        var fields = eventView.getFields();
        if (titles && titles.length) {
            // Slice to match length of given titles
            columnOrder = columnOrder.slice(0, titles.length);
        }
        var resultsRow = columnOrder.map(function (column, index) {
            var _a;
            var field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            var fieldName = getAggregateAlias(field);
            var fieldType = tableMeta[fieldName];
            var fieldRenderer = getFieldRenderer(field, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            var target = (_a = generateLink === null || generateLink === void 0 ? void 0 : generateLink[field]) === null || _a === void 0 ? void 0 : _a.call(generateLink, organization, row, location.query);
            if (target) {
                rendered = (<Link data-test-id={"view-" + fields[index]} to={target}>
            {rendered}
          </Link>);
            }
            var isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            var key = rowIndex + ":" + column.key + ":" + index;
            rendered = isNumeric ? (<GridCellNumber>{rendered}</GridCellNumber>) : (<GridCell>{rendered}</GridCell>);
            if (handleCellAction) {
                rendered = (<CellAction column={column} dataRow={row} handleCellAction={handleCellAction(column)}>
            {rendered}
          </CellAction>);
            }
            return <BodyCellContainer key={key}>{rendered}</BodyCellContainer>;
        });
        if (baselineTransactionName) {
            if (baselineData) {
                var currentTransactionDuration = Number(row['transaction.duration']) || 0;
                var duration = baselineData['transaction.duration'];
                var delta = Math.abs(currentTransactionDuration - duration);
                var relativeSpeed = currentTransactionDuration < duration
                    ? t('faster')
                    : currentTransactionDuration > duration
                        ? t('slower')
                        : '';
                var target = getTransactionComparisonUrl({
                    organization: organization,
                    baselineEventSlug: generateEventSlug(baselineData),
                    regressionEventSlug: generateEventSlug(row),
                    transaction: baselineTransactionName,
                    query: location.query,
                });
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={rowIndex + "-baseline"} style={{ textAlign: 'right' }}>
            <GridCell>
              <Link to={target} onClick={handleBaselineClick}>
                {getDuration(delta / 1000, delta < 1000 ? 0 : 2) + " " + relativeSpeed}
              </Link>
            </GridCell>
          </BodyCellContainer>);
            }
            else {
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={rowIndex + "-baseline"}>
            {'\u2014'}
          </BodyCellContainer>);
            }
        }
        return resultsRow;
    };
    TransactionsTable.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData, columnOrder = _a.columnOrder;
        var cells = [];
        if (isLoading) {
            return cells;
        }
        if (!tableData || !tableData.meta || !tableData.data) {
            return cells;
        }
        tableData.data.forEach(function (row, i) {
            // Another check to appease tsc
            if (!tableData.meta) {
                return;
            }
            cells = cells.concat(_this.renderRow(row, i, columnOrder, tableData.meta));
        });
        return cells;
    };
    TransactionsTable.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        // Custom set the height so we don't have layout shift when results are loaded.
        var loader = <LoadingIndicator style={{ margin: '70px auto' }}/>;
        return (<PanelTable isEmpty={!hasResults} emptyMessage={t('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding loader={loader}>
        {this.renderResults()}
      </PanelTable>);
    };
    return TransactionsTable;
}(React.PureComponent));
var HeadCellContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var BodyCellContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  ", ";\n"], ["\n  padding: ", " ", ";\n  ", ";\n"])), space(1), space(2), overflowEllipsis);
var StyledIconQuestion = styled(QuestionTooltip)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"], ["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"])));
export default TransactionsTable;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionsTable.jsx.map