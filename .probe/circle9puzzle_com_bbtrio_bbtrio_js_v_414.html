BBTRIO = {};
Object.assign(BBTRIO, BLUEBERRY);
BBTRIO.hideRowColumnBlockClues = true;
BBTRIO.pairRuleEnabled = false;
BBTRIO.antiKingRuleEnabled = false;
BBTRIO.antiOrthogonalRuleEnabled = false;
BBTRIO.options = { 
    hideRowColumnBlockClues: BBTRIO.hideRowColumnBlockClues,
    pairRuleEnabled: BBTRIO.pairRuleEnabled, 
    antiKingRuleEnabled: BBTRIO.antiKingRuleEnabled,
    antiOrthogonalRuleEnabled: BBTRIO.antiOrthogonalRuleEnabled,
    hideSameNPips: true,
};
BBTRIO.createModel = (desc) => {
    const options = BBTRIO.options;
    const model = BLUEBERRY.createModel(desc, options);
    const s = BBTRIO.solutions[desc];
    const desc_ = JSON.parse(desc);
    if (desc_.solution !== undefined) {
        model.solutionState = BBTRIO.unstringifyState(model, desc_.solution);
    } else if (s !== undefined) {
        // TODO:jkd remove
        model.solutionState = BBTRIO.unstringifyState(model, s);
    } else {
        // XXX:jkd remove
        const state1 = BBTRIO.createInitialState(model);
        const soln = BBTRIO.solve.trySolvePuzzle(model, state1, "Advanced");
        model.solutionState = state1;
    }
    return model;
};