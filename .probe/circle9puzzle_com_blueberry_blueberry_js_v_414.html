// TODO:jkd re-implement Blueberry and friends in Puzzlelab

BLUEBERRY = {};
BLUEBERRY.settings = [
    { id: "autoCheck", text: "Check", kind: "choice", values: ["Auto", "Manual"], defaultValue: "Auto" },
    // { id: "style", text: "Style", kind: "choice", values: ["A", "B"], defaultValue: "A" },
];
BLUEBERRY.enableAutoCheckSolved = true;
BLUEBERRY.createModel = (desc_, options) => {
    if (options == undefined) {
        options = { 
            hideRowColumnBlockClues: false, 
            pairRuleEnabled: false,
            antiKingRuleEnabled: false,
            antiOrthogonalRuleEnabled: false,
        };
    }
    const desc = JSON.parse(desc_);
    { // TODO:jkd mark this in the puzzle data instead

        function allSameValue(values) {
            let set = new Set(values);
            if (set.size == 1) {
                let same_value = Array.from(set)[0];
                return same_value;
            }
            return undefined; // not all the same value
        }
        
        { // if all row and column clues are the same number, hide them.
            function testAllRowColCluesSameValue(desc) {
                function test() {
                    let values = [
                        ...desc.rowClues.slice(0,desc.numRows), 
                        ...desc.columnClues.slice(0,desc.numColumns), 
                        ...desc.blockClues.slice(0,desc.blockClues.length - 1)];
                    let same_value = allSameValue(values);
                    for (let value of values) {
                        if (same_value === undefined) { same_value = value; }
                        if (same_value !== value) { return false; }
                    }
                    return same_value;
                }
                let v1 = test(desc.rowClues);
                let v2 = test(desc.columnClues);
                let v3 = test(desc.blockClues);
                if (v1 === false || v2 === false || v3 === false) { return false; }
                if (v1 === v2 && v1 === v3) { return v1; }
                return undefined;
            }
            let v = testAllRowColCluesSameValue(desc);
            if (v !== false) {
                options.hideRowColumnBlockClues = true;
                options.sameNPerRowCol = v;
            }
        }
        // { // if all cells are in the same block, hide the bold lines.
        //     let sameBlock = allSameValue(desc.blocks);
        //     if (sameBlock != null) {
        //         options.hideBlockLines = true;
        //     }
        // }
    }
    const grid = PUZZLEUTIL.model.createGrid(desc.size.rows, desc.size.columns);
    const allGroups = [];
    const cellsOfGroup = [];
    const blocks = {};
    const blockFromCell = {};
    const cellsOfBlock = {};
    for (let r = 0; r < grid.numRows; ++r) {
        allGroups.push(`R${r + 1}`);
    }
    for (let c = 0; c < grid.numColumns; ++c) {
        allGroups.push(`C${c + 1}`);
    }
    let numBlocks = 0;
    for (let r = 0; r < grid.numRows; ++r) {
        for (let c = 0; c < grid.numColumns; ++c) {
            const cell = grid.cellInRowColumn(r + 1, c + 1);
            const index = c + r * grid.numColumns;
            const b = desc.blocks[index];
            if (b + 1 >= numBlocks) {
                numBlocks = b + 1;
            }
            const block = `B${b + 1}`;
            blockFromCell[cell] = block;
            blocks[block] = true;
            if (cellsOfBlock[block] == undefined) {
                cellsOfBlock[block] = {};
            }
            cellsOfBlock[block][cell] = true;
        }
    }
    for (let b = 0; b < numBlocks; ++b) {
        allGroups.push(`B${b + 1}`);
    }
    allGroups.forEach(group => {
        cellsOfGroup[group] = {};
    });
    Object.keys(grid.cells).forEach(cell => {
        cellsOfGroup[grid.rowOfCell[cell]][cell] = true;
        cellsOfGroup[grid.columnOfCell[cell]][cell] = true;
        cellsOfGroup[blockFromCell[cell]][cell] = true;
    });
    const clueFromCell = {};
    const clueFromGroup = {};
    desc.rowClues.forEach((clue, r) => {
        if (typeof(clue) == "number") {
            const row = `R${r + 1}`;
            clueFromGroup[row] = clue;
        }
    });
    desc.columnClues.forEach((clue, c) => {
        if (typeof(clue) == "number") {
            const column = `C${c + 1}`;
            clueFromGroup[column] = clue;
        }
    });
    desc.blockClues.forEach((clue, blockIndex) => {
        if (typeof(clue) == "number") {
            const block = `B${blockIndex + 1}`;
            clueFromGroup[block] = clue;
        }
    });
    const cellFromNumberGroup = {};
    if (desc.cellClues != undefined) {
        desc.cellClues.forEach((clue, cellIndex) => {
            if (typeof(clue) == "number") {
                const r = Math.floor(cellIndex / grid.numColumns);
                const c = Math.floor(cellIndex % grid.numColumns);
                const cell = `R${r + 1}C${c + 1}`;
                clueFromCell[cell] = clue;
                const group = `N-${cell}`;
                allGroups.push(group);
                cellsOfGroup[group] = {};
                clueFromGroup[group] = clue;
                cellFromNumberGroup[group] = cell;
                const neighbors = grid.orthogonalAndDiagonalNeighborsOfCell[cell];
                Object.keys(neighbors).forEach(neighbor => {
                    cellsOfGroup[group][neighbor] = true;
                });
                cellsOfGroup[group][cell] = true;
            }
        });
    }
    const groupsFromCell = {};
    Object.keys(grid.cells).forEach(cell => {
        groupsFromCell[cell] = {};
    });
    allGroups.forEach(group => {
        const cells = cellsOfGroup[group];
        Object.keys(cells).forEach(cell => {
            groupsFromCell[cell][group] = true;
        });
    });
    const isTrio = options.hideRowColumnBlockClues;
    const model = { 
        grid, 
        allGroups, 
        blockFromCell, 
        cellsOfBlock, 
        cellsOfGroup, 
        clueFromCell, 
        clueFromGroup, 
        groupsFromCell,
        cellFromNumberGroup, 
        options, 
        isTrio
    };
    if (desc.solution !== undefined) {
        model.solutionState = BLUEBERRY.unstringifyState(model, desc.solution);
    }
    if (model.solutionState === undefined) {
        // XXX:jkd remove.
        // This is slow.
        // Solve all the puzzles and store their solutions inside of them.
        const state1 = BLUEBERRY.createInitialState(model);
        const soln = BLUEBERRY.solve.trySolvePuzzle(model, state1, "Advanced");
        model.solutionState = state1;
    }
    return model;
};
BLUEBERRY.descFromModel = (model) => {
    let desc = {};
    desc.size = {rows: model.grid.numRows, columns: model.grid.numColumns};
    desc.rowClues = [];
    desc.columnClues = [];
    desc.blockClues = [];
    for (let r = 1; r <= model.grid.numRows; r += 1) {
        const group = `R${r}`;
        const clue = model.clueFromGroup[group];
        desc.rowClues.push(clue === undefined ? null : clue);
    }
    for (let c = 1; c <= model.grid.numColumns; c += 1) {
        const group = `C${c}`;
        const clue = model.clueFromGroup[group];
        desc.columnClues.push(clue === undefined ? null : clue);
    }
    for (let b = 1; /**/; b += 1) {
        const group = `B${b}`;
        if (model.cellsOfBlock[group] === undefined) {
            break;
        }
        const clue = model.clueFromGroup[group];
        desc.blockClues.push(clue === undefined ? null : clue);
    }
    desc.blocks = [];
    Object.keys(model.grid.cells).forEach(cell => {
        const block = model.blockFromCell[cell];
        const blockNumber = Number(block.slice(1));
        desc.blocks.push(blockNumber - 1);
    });
    desc.cellClues = [];
    Object.keys(model.grid.cells).forEach(cell => {
        let clue = model.clueFromCell[cell];
        if (model.clueFromGroup[`N-${cell}`] === undefined) { // TODO:jkd is this correct?
            clue = null;
        } 
        desc.cellClues.push(clue === undefined ? null : clue);
    });
    {
        const state = BLUEBERRY.createInitialState(model);
        BLUEBERRY.solve.trySolvePuzzle(model, state, "Advanced");
        const check = BLUEBERRY.checkSolved(model, state);
        console.assert(check.status === "solved");
        if (check.status === "solved") {
            desc.solution = BLUEBERRY.stringifyState(model, state);
        }
    }
    return JSON.stringify(desc);
};
BLUEBERRY.createInitialState = (model) => {
    const state = { cells: {} };
    Object.keys(model.grid.cells).forEach(cell => {
        if (model.clueFromCell[cell] != undefined) {
            state.cells[cell] = "x";
        } else {
            state.cells[cell] = "_";
        }
    });
    return state;
};
BLUEBERRY.doCommand = (model, state, view, command) => {
    const [cell, s1, s2] = command;
    if (view === undefined) {
        state.cells[cell] = s2;
    } else {
        const visuals1 = BLUEBERRY.calcVisuals(view);
        state.cells[cell] = s2;
        const visuals2 = BLUEBERRY.calcVisuals(view);
        BLUEBERRY.refreshView(view);
        BLUEBERRY.animateBetweenVisuals(view, visuals1, visuals2, /*enableErrorDelay=*/true);
    }
    {
    }
};
BLUEBERRY.undoCommand = (model, state, view, command) => {
    const [cell, s1, s2] = command;
    BLUEBERRY.doCommand(model, state, view, [cell, s2, s1]);
};
BLUEBERRY.checkSolved = (model, state) => {
    const errorGroups = {};
    const satisfiedGroups = {};
    const satisfied2Groups = {};
    const countsByStateFromGroup = {};
    model.allGroups.forEach(group => {
        const clue = model.clueFromGroup[group];
        if (clue == undefined) {
            satisfiedGroups[group] = true;
        } else {
            let cellsInGroup;
            if (group.startsWith("R")) {
                cellsInGroup = model.grid.cellsOfRow[group];
            } else if (group.startsWith("C")) {
                cellsInGroup = model.grid.cellsOfColumn[group];
            } else if (group.startsWith("B")) {
                cellsInGroup = model.cellsOfBlock[group];
            } else if (group.startsWith("N")) {
                cellsInGroup = model.cellsOfGroup[group];
            }
            const countsByState = PUZZLEUTIL.model.countCellsByState(cellsInGroup, state.cells, ["_", "x", "o"]);
            const error = (countsByState["o"] + countsByState["_"] < clue || countsByState["o"] > clue);
            const satisfied = (countsByState["o"] == clue);
            if (error) {
                errorGroups[group] = true;
            }
            if (satisfied) {
                satisfiedGroups[group] = true;
            }
            if (satisfied && countsByState["_"] == 0) {
                satisfied2Groups[group] = true;
            }
            countsByStateFromGroup[group] = countsByState;
        }
    });
    const errorCells = {};
    Object.keys(errorGroups).forEach(group => {
        const cells = model.cellsOfGroup[group];
        Object.keys(cells).forEach(cell => {
            errorCells[cell] = true;
        });
    });
    // if (model.options.pairRuleEnabled) {
    //     const info = PUZZLEUTIL.model.findIslands(
    //         model.grid.cells, 
    //         (cell1, cell2) => {
    //             const cellState1 = state.cells[cell1];
    //             const cellState2 = state.cells[cell2];
    //             const isBerry1 = cellState1 === "o";
    //             const isBerry2 = cellState2 === "o";
    //             return isBerry1 === isBerry2;
    //         },
    //         model.grid.orthogonalNeighborsOfCell
    //     );
    //     Object.entries(info.cellsOfIsland).forEach(([island, cells]) => {
    //         const cellsK = Object.keys(cells);
    //         if (cellsK.length > 0 && state.cells[cellsK[0]] === "o") {
    //             if (cellsK.length === 1) {
    //                 const cell = cellsK[0];
    //                 const neighbors = Object.keys(model.grid.orthogonalNeighborsOfCell[cell]);
    //                 const numUndecidedNeighbors = neighbors.reduce(
    //                     (count, neighbor) => {
    //                         if (state.cells[neighbor] === "_") {
    //                             count += 1;
    //                         }
    //                         return count;
    //                     }, 
    //                     0
    //                 );
    //                 if (numUndecidedNeighbors === 0) {
    //                     errorCells[cell] = true;
    //                 }
    //             } else if (cellsK.length > 2) {
    //                 cellsK.forEach(cell => { errorCells[cell] = true; });
    //             }
    //         }
    //     });
    // }
    let numUnpaired = 0;
    if (model.options.pairRuleEnabled) {
        Object.keys(model.grid.cells).forEach(cell => {
            if (state.cells[cell] === "o") {
                const neighbors = model.grid.orthogonalNeighborsOfCell[cell];
                const counts = PUZZLEUTIL.model.countCellsByState(neighbors, state.cells, ["_", "x", "o"]);
                if (counts["o"] !== 1) {
                    numUnpaired += 1;
                    if (counts["o"] > 1) {
                        errorCells[cell] = true;
                    }
                    if (counts["o"] === 0 && counts["_"] === 0) {
                        errorCells[cell] = true;
                    }
                }
            }
        });
    }
    function noTouch(neighborKey) {
        Object.keys(model.grid.cells).forEach(cell => {
            if (state.cells[cell] === "o") {
                const neighbors = model.grid[neighborKey][cell];
                const counts = PUZZLEUTIL.model.countCellsByState(neighbors, state.cells, ["_", "x", "o"]);
                if (counts["o"] !== 0) {
                    errorCells[cell] = true;
                }
            }
        });
    }
    if (model.options.antiKingRuleEnabled) {
        noTouch("orthogonalAndDiagonalNeighborsOfCell");
    }
    if (model.options.antiOrthogonalRuleEnabled) {
        noTouch("orthogonalNeighborsOfCell");
    }
    const countsByState = PUZZLEUTIL.model.countCellsByState(model.grid.cells, state.cells, ["_", "x", "o"]);
    const isError = (Object.keys(errorCells).length > 0);
    const isComplete = 
        (Object.keys(satisfiedGroups).length == model.allGroups.length) && 
        numUnpaired === 0; 
        //&& countsByState["_"] === 0; /* TODO:jkd this is a hack to make the generator work. Remove */;
    const status = isError ? "error" : isComplete ? "solved" : "ok";
    const compareWithSolution = model.solutionState === undefined 
        ? undefined 
        : PUZZLEUTIL.model.compareCellStatesToSolution(model.grid.cells, state.cells, model.solutionState.cells);
    return { status, compareWithSolution, errorGroups, errorCells, satisfiedGroups, satisfied2Groups, countsByState, countsByStateFromGroup };
};
BLUEBERRY.stringifyState = (model, state) => {
    return PUZZLEUTIL.model.stringifyCellStates(model.grid.cells, state.cells);
};
BLUEBERRY.unstringifyState = (model, string) => {
    const state = {}
    state.cells = PUZZLEUTIL.model.unstringifyCellStates(model.grid.cells, string);
    return state;
};
BLUEBERRY.getPuzzleId = (desc) => {
    return desc;
};
BLUEBERRY.createView = (model, state, scale, isSolution) => {
    const graphics_folder = '2';
    const graphics_ext = 'png';
    scale = scale ?? 1;
    scale *= 1.25;
    const cellSize = 40;
    const numExtraRows = model.options.hideRowColumnBlockClues ? 0 : 1;
    const numExtraColumns = model.options.hideRowColumnBlockClues ? 0 : 1;
    const spaceAbove = model.options.sameNPerRowCol ? 20 : 0;
    const width = cellSize * (model.grid.numColumns + numExtraColumns) + 10;
    const height = cellSize * (model.grid.numRows + numExtraRows)      + 10 + spaceAbove;
    const offsetX = model.options.hideRowColumnBlockClues ? 0 : -15;
    const offsetY = model.options.hideRowColumnBlockClues ? spaceAbove : -10;
    const svg = PUZZLEUTIL.view.createSvg(width, height, scale);
    // svg.style['background-color'] = 'white';
    // svg.style['margin'] = '8px';
    // svg.style['padding'] = '8px';
    // svg.style['outline'] = '1pt solid silver';
    const view = {};
    view.animator = PUZZLEUTIL.view.createAnimator();
    view.root = svg;
    view.svg = svg;
    view.model = model;
    view.state = state;
    view.refreshClues = () => {
        let check = BLUEBERRY.checkSolved(view.model, view.state);
        if (model.options.hideRowColumnBlockClues) {
        } else {
            for (let r = 0; r < model.grid.numRows; ++r) {
                const row = `R${r + 1}`;
                const clue = model.clueFromGroup[row];
                if (clue != undefined) {
                    const count = check.countsByStateFromGroup[row]['o'];
                    view.numbersLeft[`${row}C1`].textContent = `${clue/* - count*/}`;
                }
            }
            for (let c = 0; c < model.grid.numColumns; ++c) {
                const column = `C${c + 1}`;
                const clue = model.clueFromGroup[column];
                if (clue != undefined) {
                    const count = check.countsByStateFromGroup[column]['o'];
                    view.numbersAbove[`R1${column}`].textContent = `${clue/* - count*/}`;
                }
            }
        }
    };
    { // clues outside the board
        view.grid2 = PUZZLEUTIL.view.createGrid(svg, model.grid.numRows, 1, cellSize, false, false, [0 + offsetX, cellSize + offsetY]);
        view.numbersLeft = PUZZLEUTIL.view.createText(svg, view.grid2, "fill: var(--theme-text);");
        view.grid3 = PUZZLEUTIL.view.createGrid(svg, 1, model.grid.numColumns, cellSize, false, false, [cellSize + offsetX, 0 + offsetY]);
        view.numbersAbove = PUZZLEUTIL.view.createText(svg, view.grid3, "fill: var(--theme-text);");
        view.refreshClues();
    }
    view.grid = PUZZLEUTIL.view.createGrid(
        svg, 
        model.grid.numRows, 
        model.grid.numColumns, 
        cellSize, 
        false, 
        false, 
        model.options.hideRowColumnBlockClues 
            ? [2 + offsetX, 2 + offsetY] 
            : [cellSize + offsetX, cellSize + offsetY], 
    );
    Object.values(view.grid.cells).forEach(cell => {
        cell.e.classList.add("blueberry-cell");
    });
    view.boxFromCell = {};
    {
        let g = createEl({
            tag:'g',
            style: {
                // 'filter': 'drop-shadow(3px 3px 0px #0004)',
                'pointer-events': 'none',
            },
        });
        svg.appendChild(g);
        for (let cell of Object.keys(model.grid.cells)) {
            let cellinfo = view.grid.cells[cell];
            let el = createEl({
                tag: "image",
                href: `../blueberry/${graphics_folder}/box.${graphics_ext}`,
                width: cellSize,
                height: cellSize,
                x: cellinfo.center[0] - cellSize/2,
                y: cellinfo.center[1] - cellSize/2,
                class: ["blueberry-box"],
                style: {
                    "transform-origin": "center",
                    "transform-box": "fill-box",
                    "pointer-events": "none",
                    visibility: "hidden",
                },
            });
            g.appendChild(el);
            view.boxFromCell[cell] = el;
        }
    }
    view.berryImageFromCell = {};
    for (let cell of Object.keys(model.grid.cells)) {
        let cellinfo = view.grid.cells[cell];
        let el = createEl({
            tag: "image",
            href: model.options.pairRuleEnabled ? 
                `../blueberry/${graphics_folder}/cherry.${graphics_ext}` : 
                `../blueberry/${graphics_folder}/berry.${graphics_ext}`,
            width: cellSize,
            height: cellSize,
            x: cellinfo.center[0] - cellSize/2,
            y: cellinfo.center[1] - cellSize/2,
            style: {
                "transform-origin": "center",
                "transform-box": "fill-box",
                "pointer-events": "none",
                visibility: "hidden",
            },
        });
        svg.appendChild(el);
        view.berryImageFromCell[cell] = el;
    }
    view.gridLinesThinColor = "var(--theme-blueberry-grid-lines-thin)";
    const thinLineStyle = `stroke-width: 1px; stroke: ${view.gridLinesThinColor}; opacity: 100%;`;
    view.thinEdges = PUZZLEUTIL.view.createEdges(svg, view.grid, thinLineStyle);
    PUZZLEUTIL.view.refreshEdges(svg, view.thinEdges, () => true);
    {
        let display = model.options.hideBlockLines ? 'none' : '';
        view.edges = PUZZLEUTIL.view.createEdges(svg, view.grid, 
            `stroke-width: 2pt; stroke: var(--theme-blueberry-block-outline); stroke-linecap: square; display: ${display}`);
    }
    view.numbers = PUZZLEUTIL.view.createText(svg, view.grid, "font-size: 28px;");
    view.berryRadius = cellSize * 0.22;
    // view.berryRadius = cellSize * 0.25;
    view.numbersCorner = PUZZLEUTIL.view.createTextCorner(svg, view.grid, "");
    view.blackout = PUZZLEUTIL.view.createRects(svg, view.grid, "visibility: hidden;");
    view.blackout.g.style["opacity"] = "70%";
    view.clueRectEdges = PUZZLEUTIL.view.createEdges(svg, view.grid, 'stroke-width: 3pt; stroke: var(--theme-blueberry-clue-rect-stroke);');
    Object.entries(model.clueFromCell).forEach(([cell, clue]) => {
        const e = view.numbers[cell];
        e.textContent = `${clue}`;
        const rect = view.grid.cells[cell].e;
        // rect.style.pointerEvents = "none";
    });
    const cellOfBlockClue = {};
    view.cellOfBlockClue = cellOfBlockClue;
    if (model.options.hideRowColumnBlockClues) {
    } else {
        Object.keys(model.grid.cells).forEach(cell => {
            const block = model.blockFromCell[cell];
            if (cellOfBlockClue[block] == undefined) {
                cellOfBlockClue[block] = cell;
                const text = view.numbersCorner[cell];
                const clue = model.clueFromGroup[block];
                if (clue != undefined) {
                    text.textContent = `${clue}`;
                }
            }
        });
    }
    if (!model.options.hideSameNPips && model.options.sameNPerRowCol != null) {
        const berryURL = model.options.pairRuleEnabled ? 
            `../blueberry/${graphics_folder}/cherry.${graphics_ext}` : 
            `../blueberry/${graphics_folder}/berry.${graphics_ext}`;
        let w = view.berryRadius * 2 * 1.5;
        let spacing = w * 0.65;
        for (let i of integers(1, model.options.sameNPerRowCol)) {
            let el = createEl({
                tag: "image",
                href: berryURL,
                x: width - spacing * i - spacing*0.3,
                y: -3,
                width: w,
                height: w,
            });
            svg.appendChild(el);
        }
    }
    const toggleClueRect = (cell) => {
        if (view.cluesShowingRectangle.has(cell)) {
            view.cluesShowingRectangle.delete(cell);
        } else {
            view.cluesShowingRectangle = new Set([cell]);
        }
        BLUEBERRY.refreshView(view);
    };
    const noninteractiveFromCell = mapObject(
        model.grid.cells, 
        // cell => model.clueFromCell[cell] !== undefined ? toggleClueRect : false);
        cell => model.clueFromCell[cell] !== undefined);
    view.cluesShowingRectangle = new Set();
    PUZZLEUTIL.view.setGridDownDragUpListenersToCycleCellState(view, view.grid, ["_", "x", "o"], noninteractiveFromCell);
    PUZZLEUTIL.view.setDefaultSettings(view, BLUEBERRY.settings);
    if (isSolution) {
        view.settingsValues["autoCheck"] = "Manual";
    }
    return view;
};
BLUEBERRY.refreshView = (view) => {
    // {
    //     const root = document.querySelector(":root");
    //     const styleName = view.settingsValues["style"];
    //     ["A","B"].forEach(s => {
    //         const n = `style-${s}`;
    //         if (styleName === s) {
    //             root.classList.add(n);
    //         } else {
    //             root.classList.remove(n);
    //         }
    //     });
    // } 
    const model = view.model;
    const hint = view.hint;
    const enableErrorDelay = view.check == null;
    const visuals = BLUEBERRY.calcVisuals(view);
    BLUEBERRY.animateBetweenVisuals(view, visuals, visuals, enableErrorDelay);
    Object.entries(view.blackout.rectFromCell).forEach(([cell, e]) => {
        const blackedOut = hint === undefined ? false : hint.cells[cell] === undefined;
        e.style["visibility"] = blackedOut ? "visible" : "hidden";
    });
    const hintGroup = hint !== undefined ? hint.group : undefined;
    if (hintGroup !== undefined) {
        [view.edges].forEach(edges => {
            PUZZLEUTIL.view.refreshEdgesSlow(view.svg, edges, (a, b) => {
                const block_a = model.blockFromCell[a];
                const block_b = model.blockFromCell[b];
                const isEdge = (block_a !== block_b);
                const style = block_a === hintGroup || block_b === hintGroup
                    ? "stroke-width: 3px;"
                    : ""
                return [isEdge, style];
            });
        });
    } else {
        [view.edges].forEach(edges => {
            PUZZLEUTIL.view.refreshEdges(view.svg, edges, (a, b) => {
                return (model.blockFromCell[a] != model.blockFromCell[b]);
            });
        });
    }
    view.refreshClues();
    PUZZLEUTIL.view.refreshEdges(view.svg, view.clueRectEdges, (cell1, cell2) => {
        if (cell1 == null || cell2 == null) { return false; }
        for (let cell of Array.from(view.cluesShowingRectangle)) {
            let cellsAroundClue = view.model.cellsOfGroup[`N-${cell}`];
            let in1 = cellsAroundClue[cell1] != null;
            let in2 = cellsAroundClue[cell2] != null;
            if (in1 !== in2) { return true; }
        }
        return false;
    });
};
BLUEBERRY.calcVisuals = (view) => {
    let check = view.check;
    const hint = view.hint;
    if (view.settingsValues["autoCheck"] === "Auto") {
        if (check === undefined) {
            check = BLUEBERRY.checkSolved(view.model, view.state);
        }
    }
    const model = view.model;
    const state = view.state;
    const colorFromCell = {};
    const errorColorFromCell = {};
    const dotVisibleFromCell = {};
    const berryVisibleFromCell = {};
    const textColorFromGroup = {};
    const textWeightFromGroup = {};
    const textOpacityFromGroup = {};
    Object.keys(model.grid.cells).forEach(cell => {
        const s = state.cells[cell];
        colorFromCell[cell] = 'var(--theme-blueberry-cell)';
        const isErrorCell = check !== undefined && check.errorCells[cell] !== undefined;
        if (isErrorCell) {
            errorColorFromCell[cell] = "var(--theme-blueberry-error-cell)";
        }
        dotVisibleFromCell[cell] = s === "_";
        berryVisibleFromCell[cell] = s === "o";
    });
    const isNumberOutsideBoard = (group) => {
        return group.startsWith("R") || group.startsWith("C");
    };
    model.allGroups.forEach(group => {
        const isSatisfiedGroup = check !== undefined && check.satisfied2Groups[group];
        const isPrimaryHintGroup = hint !== undefined && group === hint.group;
        const isClueAndShowingRect = () => {
            if (group.startsWith('N-')) {
                let cell = group.slice(2);
                if (view.cluesShowingRectangle.has(cell)) {
                    return true;
                }
            }
            return false;
        };
        const weight = isPrimaryHintGroup || isClueAndShowingRect() ? "bold" : "";
        let clueCellOpened = false;
        if (group.startsWith("B")) {
            const cell = view.cellOfBlockClue[group];
            clueCellOpened = (view.state.cells[cell] !== "_");
        } else if (group.startsWith("N")) {
            const cell = model.cellFromNumberGroup[group];
            clueCellOpened = (view.state.cells[cell] !== "_");
        }
        textColorFromGroup[group] = isNumberOutsideBoard(group) 
            ? "var(--theme-blueberry-clue-text-outside-board)" 
            : `var(--theme-blueberry-clue-text-inside-board${clueCellOpened?'-opened':''})`;
        textWeightFromGroup[group] = weight;
        textOpacityFromGroup[group] = isSatisfiedGroup ? "25%" : "100%";
    });
    const visuals = { check, colorFromCell, errorColorFromCell, dotVisibleFromCell, berryVisibleFromCell, textColorFromGroup, textWeightFromGroup, textOpacityFromGroup };
    return visuals;
};
BLUEBERRY.animateBetweenVisuals = (view, visuals1, visuals2, enableErrorDelay) => {
    const model = view.model;
    const state = view.state;
    const errorDelay = enableErrorDelay && view.settingsValues["autoCheck"] === "Auto" ? 1000 : 1;
    Object.keys(model.grid.cells).forEach(cell => {
        const cellColor1 = visuals1.colorFromCell[cell];
        const cellColor2 = visuals2.colorFromCell[cell];
        const cellErrorColor2 = visuals2.errorColorFromCell[cell];
        const dotVisible1 = visuals1.dotVisibleFromCell[cell];
        const dotVisible2 = visuals2.dotVisibleFromCell[cell];
        const berryVisible1 = visuals1.berryVisibleFromCell[cell];
        const berryVisible2 = visuals2.berryVisibleFromCell[cell];
        let isError1 = false;
        let isError2 = false;
        if (visuals1.check !== undefined && visuals2.check !== undefined) {
            isError1 = visuals1.check.errorCells[cell] !== undefined;
            isError2 = visuals2.check.errorCells[cell] !== undefined;
        }
        view.boxFromCell[cell].style.visibility = dotVisible2 ? "visible" : "hidden";
        {
            const rect = view.grid.cells[cell].e;
            const e = rect;
            view.animator.playKeyframes(
                [
                    {
                        duration: 150,
                        fn: (t) => {
                            t = 1 - Math.pow(1 - t, 2);
                            // e.style["fill"] = cssColorMix(cellColor1, cellColor2, t);
                            e.style["fill"] = cellColor2;
                        }
                    }
                ],
                e,
            );
            if (isError2) {
                view.animator.playKeyframes(
                    [
                        {
                            duration: errorDelay,
                            fn: (t) => {},
                        },
                        {
                            duration: 150,
                            fn: (t) => {
                                t = 1 - Math.pow(1 - t, 2);
                                // e.style["fill"] = cssColorMix(cellColor1, cellErrorColor2, t);
                                e.style["fill"] = cellErrorColor2;
                            }
                        }
                    ],
                    e, enableErrorDelay ? "append" : "truncate"
                );
            }
        }
        {
            const berry = view.berryImageFromCell[cell];
            berry.style["visibility"] = berryVisible2 ? "visible" : "hidden";
            if (berryVisible2 && !berryVisible1) {
                const e = berry;
                view.animator.playKeyframes(
                    [
                        {
                            duration: 100,
                            fn: (t) => {
                                t = Math.pow(t, 1);
                                const scale = lerp(1.3, 1, t);
                                // const radius = scale * view.berryRadius; 
                                // e.setAttribute("r", `${radius}px`);
                                e.style['transform'] = `scale(${scale})`;
                            }
                        }
                    ],
                    e
                );
            }
        }
    });
    model.allGroups.forEach(group => {
        const textE = BLUEBERRY.textFromGroup(view, group);
        if (textE !== undefined) {
            const color1 = visuals1.textColorFromGroup[group];
            const color2 = visuals2.textColorFromGroup[group];
            const weight1 = visuals1.textWeightFromGroup[group];
            const weight2 = visuals2.textWeightFromGroup[group];
            const opacity1 = visuals1.textOpacityFromGroup[group];
            const opacity2 = visuals2.textOpacityFromGroup[group];
            let isError1 = false;
            let isError2 = false;
            if (visuals1.check !== undefined && visuals2.check !== undefined) {
                isError1 = visuals1.check.errorGroups[group] !== undefined;
                isError2 = visuals2.check.errorGroups[group] !== undefined;
            }
            const e = textE;
            view.animator.playKeyframes(
                [
                    {
                        duration: 150,
                        fn: (t) => {
                            textE.style["fill"] = color2;
                            textE.style["font-weight"] = weight2;
                            textE.style["opacity"] = opacity2;
                        }
                    }
                ],
                e
            );
            if (isError2) {
                view.animator.playKeyframes(
                    [
                        {
                            duration: errorDelay,
                            fn: (t) => {},
                        },
                        {
                            duration: 1,
                            fn: (t) => {
                                e.style["fill"] = "var(--theme-blueberry-error-text)";
                                e.style["font-weight"] = "bold";
                                e.style["opacity"] = "100%";
                            }
                        }
                    ],
                    e, enableErrorDelay ? "append" : "truncate"
                );
            }
        }
    });
};
BLUEBERRY.textFromGroup = (view, group) => {
    if (group.startsWith("R")) {
        const text = view.numbersLeft[`${group}C1`];
        return text;
    } else if (group.startsWith("C")) {
        const text = view.numbersAbove[`R1${group}`];
        return text;
    } else if (group.startsWith("B")) {
        const cell = view.cellOfBlockClue[group];
        const text = view.numbersCorner[cell];
        return text;
    } else if (group.startsWith("N-")) {
        const text = view.numbers[group.slice(2)];
        return text;
    }
};
BLUEBERRY.solvedAnimationColors = [ 
    "var(--theme-blueberry-blueberry)", "silver", "beige", 
];
BLUEBERRY.hint = (model, state) => {
    const [berry, berries] = model.options.pairRuleEnabled ? ["cherry", "cherries"] : ["berry", "berries"];
    const compareWithSolution = PUZZLEUTIL.model.compareCellStatesToSolution(model.grid.cells, state.cells, model.solutionState.cells);
    if (compareWithSolution.status === "error") { return undefined; }
    const groupType = (group) => {
        if (group.startsWith("R")) { return "row"; }
        if (group.startsWith("C")) { return "column"; }
        if (group.startsWith("B")) { return "block"; }
        if (group.startsWith("N")) { return "number"; }
    };
    const groupName = (group) => {
        const t = groupType(group);
        if (t === "number") { return undefined; }
        const tCap = replaceStringCharAt(t, 0, t.slice(0, 1).toUpperCase());
        return `${tCap} ${group.slice(1)}`
    };
    const moves = BLUEBERRY.solve.findTechniques(model, state, "Advanced");
    const move = moves[0];
    if (move === undefined) { return undefined; }
    if (move.technique === "MIN" || move.technique === "MAX") {
        const primaryGroup = move.primaryGroups[0];
        const primaryGroupName = groupName(primaryGroup);
        const primaryGroupType = groupType(primaryGroup);
        const imum = (move.technique === "MIN") ? "minimum" : "maximum"; 
        const cells = {};
        const secondaryGroups = [];
        Object.entries(move.subs).forEach(([g, it]) => {
            // const groupCells = model.cellsOfGroup[g];
            // let kcount = 0;
            // Object.keys(groupCells).forEach(cell => {
            //     if (move.knowledge[cell] !== undefined) {
            //         kcount += 1;
            //     }
            // });
            if (it.inCounts["_"] > 0) {
                secondaryGroups.push(g);
            }
        });
        move.primaryGroups.forEach(g => {
            Object.keys(model.cellsOfGroup[g]).forEach(cell => {
                cells[cell] = true;
            });
        });
        secondaryGroups.forEach(g => {
            Object.keys(model.cellsOfGroup[g]).forEach(cell => {
                cells[cell] = true;
            });
        });
        const theseSubs = secondaryGroups.length === 1
            ? `this ${groupType(secondaryGroups[0])}`
            : `these ${groupType(secondaryGroups[0])}s`;
        let text;
        if (primaryGroupType === "block") {
            text = `This block requires the ${imum} number of ${berries} from each ${groupType(secondaryGroups[0])}.`;
        } else if (primaryGroupType == "number") {
            text = `This number clue requires the ${imum} number of ${berries} from ${theseSubs}.`;
        } else {
            text = `${primaryGroupName} requires the ${imum} number of ${berries} from ${theseSubs}.`;
        }
        return {move, text, cells, group: primaryGroup};
    } else if (move.technique === "FILL" || move.technique === "FULL") {
        let text = "";
        if (move.technique === "FILL") { 
            const clue = model.clueFromGroup[move.group];
            const gt = groupType(move.group);
            // if (model.isTrio && gt !== "number") {
                // text = `Fill the trio in this ${gt}.`;
            // } else {
                text = `Fill this ${gt} with ${clue} ${clue === 1 ? berry : berries}.`;
            // }
        } else if (move.technique === "FULL") {
            const clue = model.clueFromGroup[move.group];
            const gt = groupType(move.group);
            // if (model.isTrio && gt !== "number") {
                // text = `The trio is complete in this ${groupType(move.group)}.`;
            // } else {
                text = `This ${groupType(move.group)} is full with ${clue} ${clue === 1 ? berry : berries}.`;
            // }
        }
        const cells = {};
        Object.keys(model.cellsOfGroup[move.group]).forEach(cell => {
            cells[cell] = true;
        });
        return {move, text, cells, group: move.group};
    } else if (move.technique === "SHALLOW-LOOKAHEAD") {
        const cells = {};
        [Object.keys(move.knowledge)[0]].forEach(k => { cells[k] = true; } );
        const f = () => {
            const cell = Object.keys(cells)[0];
            const w = move.knowledge[cell];
            if (w === "x") {
                return `A cherry cannot be placed in this cell.`;
            } else if (w === "o") {
                return `A cherry must be placed in this cell.`;
            }
        };
        const text = f();
        const r = {move, text, cells, group: move.group};
        return r;
    } else if (move.technique === "SHALLOW-LOOKAHEAD-PAIRS") {
        const cells = {};
        [Object.keys(move.knowledge)[0]].forEach(k => { cells[k] = true; } );
        const text = `A ${berry} placed here could not pair with another cherry.`;
        const r = {move, text, cells};
        return r;
    } else if (move.technique === "PAIR-COMMONALITY") {
        const cells = {};
        [Object.keys(move.knowledge)[0]].forEach(k => { cells[k] = true; } );
        cells[move.cherryCell] = true;
        const text = `Both ways to pair with this ${berry} will eliminate this cell.`;
        const r = {move, text, cells};
        return r;
    } else if (move.technique === "COMBOS") {
        const f = () => {
            if (move.numOkCombos === 1) {
                return `There is only one way to fill this ${groupType(move.group)}.`;
            } else {
                return `Consider the possible ways to fill this ${groupType(move.group)}.`;
            }
        };
        const text = f();
        const cells = {};
        Object.keys(move.knowledge).forEach(k => { cells[k] = true; } );
        if (move.clueCell != null) { cells[move.clueCell] = true; }
        const r = {move, text, cells, group: move.group};
        return r;
    } else {
        const text = `${move.technique}`;
        const cells = {};
        Object.keys(move.knowledge).forEach(k => { cells[k] = true; } );
        const r = {move, text, cells, group: move.group};
        return r;
    }
};