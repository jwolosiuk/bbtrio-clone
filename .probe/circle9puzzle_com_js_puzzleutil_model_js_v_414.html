PUZZLEUTIL.model = {};
PUZZLEUTIL.model.createGrid = (numRows, numColumns) => {
    const grid = {
        numRows, 
        numColumns,
        cells: {},
        rowOfCell: {},
        columnOfCell: {},
        rowNumberOfCell: {},
        columnNumberOfCell: {},
        neighborOfCell: {},
        orthogonalNeighborsOfCell: {},
        diagonalNeighborsOfCell: {},
        orthogonalAndDiagonalNeighborsOfCell: {},
        cellsOfRow: {},
        cellsOfColumn: {},
        cellInRowColumn: (r, c) => {
            if (r < 1 || r > numRows || c < 1 || c > numColumns) {
                return undefined;
            }
            return `R${r}C${c}`;
        },
        hasCell: (r, c) => (r >= 1 && r <= numRows && c >= 1 && c <= numColumns),
        numberOfRow: {},
        numberOfColumn: {},
    };
    grid.indexFromCell = {};
    grid.cellFromIndex = {};
    for (let r = 1; r <= numRows; ++r) {
        for (let c = 1; c <= numColumns; ++c) {
            const cell = `R${r}C${c}`;
            const index = (c-1) + (r-1) * numColumns;
            grid.indexFromCell[cell] = index;
            grid.cellFromIndex[index] = cell;
        }
    }

    for (let r = 1; r <= numRows; ++r) {
        const id = `R${r}`;
        grid.cellsOfRow[id] = {};
        grid.numberOfRow[id] = r;
    }
    for (let c = 1; c <= numColumns; ++c) {
        const id = `C${c}`;
        grid.cellsOfColumn[id] = {};
        grid.numberOfColumn[id] = c;
    }
    for (let r = 1; r <= numRows; ++r) {
        for (let c = 1; c <= numColumns; ++c) {
            const cell = `R${r}C${c}`;
            grid.cells[cell] = true;
            grid.rowOfCell[cell] = `R${r}`;
            grid.columnOfCell[cell] = `C${c}`;
            grid.rowNumberOfCell[cell] = r;
            grid.columnNumberOfCell[cell] = c;
            grid.neighborOfCell[cell] = {};
            grid.orthogonalNeighborsOfCell[cell] = {};
            grid.diagonalNeighborsOfCell[cell] = {};
            grid.orthogonalAndDiagonalNeighborsOfCell[cell] = {};
            if (r > 1) {
                const neighbor = `R${r-1}C${c}`;
                grid.neighborOfCell[cell]["up"] = neighbor;
                grid.orthogonalNeighborsOfCell[cell][neighbor] = true;
            }
            if (r < numRows) {
                const neighbor = `R${r+1}C${c}`;
                grid.neighborOfCell[cell]["down"] = neighbor;
                grid.orthogonalNeighborsOfCell[cell][neighbor] = true;
            }
            if (c > 1) {
                const neighbor = `R${r}C${c-1}`;
                grid.neighborOfCell[cell]["left"] = neighbor;
                grid.orthogonalNeighborsOfCell[cell][neighbor] = true;
            }
            if (c < numColumns) {
                const neighbor = `R${r}C${c+1}`;
                grid.neighborOfCell[cell]["right"] = neighbor;
                grid.orthogonalNeighborsOfCell[cell][neighbor] = true;
            }
            if (r > 1 && c > 1) {
                grid.diagonalNeighborsOfCell[cell][`R${r-1}C${c-1}`] = true;
            }
            if (r < numRows && c > 1) {
                grid.diagonalNeighborsOfCell[cell][`R${r+1}C${c-1}`] = true;
            }
            if (r > 1 && c < numColumns) {
                grid.diagonalNeighborsOfCell[cell][`R${r-1}C${c+1}`] = true;
            }
            if (r < numRows && c < numColumns) {
                grid.diagonalNeighborsOfCell[cell][`R${r+1}C${c+1}`] = true;
            }
            Object.keys(grid.orthogonalNeighborsOfCell[cell]).forEach((n) => {
                grid.orthogonalAndDiagonalNeighborsOfCell[cell][n] = true;
            });
            Object.keys(grid.diagonalNeighborsOfCell[cell]).forEach((n) => {
                grid.orthogonalAndDiagonalNeighborsOfCell[cell][n] = true;
            });
            grid.cellsOfRow[`R${r}`][cell] = true;
            grid.cellsOfColumn[`C${c}`][cell] = true;
        }
    }
    return grid;
};
PUZZLEUTIL.model.cellSymmetric180 = (grid, cell) => {
    const r = grid.rowNumberOfCell[cell];
    const c = grid.columnNumberOfCell[cell];
    const rs = grid.numRows - r + 1;
    const cs = grid.numColumns - c + 1;
    return grid.cellInRowColumn(rs, cs);
};
PUZZLEUTIL.model.cellSymmetricMirrorH = (grid, cell) => {
    const r = grid.rowNumberOfCell[cell];
    const c = grid.columnNumberOfCell[cell];
    const rs = r;
    const cs = grid.numColumns - c + 1;
    return grid.cellInRowColumn(rs, cs);
};
PUZZLEUTIL.model.cellSymmetricMirrorV = (grid, cell) => {
    const r = grid.rowNumberOfCell[cell];
    const c = grid.columnNumberOfCell[cell];
    const rs = grid.numRows - r + 1;
    const cs = c;
    return grid.cellInRowColumn(rs, cs);
};
PUZZLEUTIL.model.findIslands = (cells, compareFunc, neighborsOfCell) => {
    const islandOfCell = {};
    const cellsOfIsland = {};
    const recurse = (cell, currentIsland) => {
        if (islandOfCell[cell] != undefined) {
            return;
        }
        if (currentIsland == undefined) {
            const newIsland = `${Object.keys(cellsOfIsland).length + 1}`;
            cellsOfIsland[newIsland] = {};
            currentIsland = newIsland;
        }
        cellsOfIsland[currentIsland][cell] = true;
        islandOfCell[cell] = currentIsland;
        const neighbors = neighborsOfCell[cell];
        Object.keys(neighbors).forEach((neighbor) => {
            if (compareFunc(neighbor, cell)) {
                recurse(neighbor, currentIsland);
            }
        });
    };
    Object.keys(cells).forEach((cell) => {
        recurse(cell, undefined);
    });
    return {islandOfCell, cellsOfIsland, };
};
PUZZLEUTIL.model.areIslandsNeighbors = (cellsOfIsland1, cellsOfIsland2, neighborsOfCell) => {
    let ok = false;
    Object.keys(cellsOfIsland1).forEach((cell) => {
        const neighbors = neighborsOfCell[cell];
        Object.keys(neighbors).forEach((neighbor) => {
            if (cellsOfIsland2[neighbor] != undefined) {
                ok = true;
            }
        })
    });
    return ok;
};
PUZZLEUTIL.model.countCellsByState = (cells, state, expectedStates) => {
    const r = {};
    if (expectedStates) {
        expectedStates.forEach((expectedState) => {
            r[expectedState] = 0;
        });
    }
    Object.keys(cells).forEach((cell) => {
        const s = state[cell];
        if (r[s] == undefined) {
            r[s] = 0;
        }
        r[s] += 1;
    });
    return r;
};
PUZZLEUTIL.model.splitCellsByState = (cells, state, expectedStates) => {
    const r = {};
    if (expectedStates) {
        expectedStates.forEach((expectedState) => {
            r[expectedState] = {};
        });
    }
    Object.keys(cells).forEach((cell) => {
        const s = state[cell];
        if (r[s] === undefined) {
            r[s] = {};
        }
        r[s][cell] = true;
    });
    return r;
};
PUZZLEUTIL.model.tetrominoes = {
    "Z": [[0,0],[0,1],[1,1],[1,2]],
    "S": [[0,1],[0,2],[1,0],[1,1]],
    "J": [[1,0],[1,1],[1,2],[0,0]],
    "L": [[1,2],[1,1],[1,0],[0,2]],
    "I": [[0,0],[0,1],[0,2],[0,3]],
    "O": [[0,0],[0,1],[1,0],[1,1]],
    "T": [[1,0],[1,1],[1,2],[0,1]],
};
PUZZLEUTIL.model.polyominoes = {
    "1": [[0,0]],

    "2": [[0,0],[0,1]],

    "I3": [[0,0],[0,1],[0,2]],
    "V3": [[0,0],[1,0],[0,1]],

    "I4": [[0,0],[0,1],[0,2],[0,3]],
    "L4": [[0,0],[0,1],[0,2],[1,2]],
    "O": [[0,0],[0,1],[1,0],[1,1]],
    "T4": [[0,0],[1,0],[2,0],[1,1]],
    "Z4": [[0,0],[1,0],[1,1],[2,1]],

    "F": [[1,0],[2,0],[0,1],[1,1],[1,2]],
    "I5": [[0,0],[0,1],[0,2],[0,3],[0,4]],
    "L5": [[0,0],[0,1],[0,2],[0,3],[1,3]],
    "N": [[0,0],[0,1],[0,2],[1,2],[1,3]],
    "P": [[0,0],[1,0],[0,1],[1,1],[0,2]],
    "T5": [[0,0],[1,0],[2,0],[1,1],[1,2]],
    "U": [[0,0],[1,0],[0,1],[0,2],[1,2]],
    "V5": [[0,0],[1,0],[2,0],[0,1],[0,2]],
    "W": [[0,0],[0,1],[1,1],[1,2],[2,2]],
    "X": [[1,0],[0,1],[1,1],[2,1],[1,2]],
    "Y": [[0,0],[0,1],[1,1],[0,2],[0,3]],
    "Z5": [[0,0],[1,0],[1,1],[1,2],[2,2]],
};
PUZZLEUTIL.model.calcPolyominoesRotation = (polyominoes) => {
    const polyominoesT = {};
    Object.entries(polyominoes).forEach(([polyominoName, polyomino]) => {
        polyominoesT[polyominoName] = [];
        for (let rotation = 0; rotation < 4; rotation += 1) {
            const polyT = PUZZLEUTIL.model.translatePolyominoToOrigin(
                PUZZLEUTIL.model.rotatePolyomino(polyomino, rotation)
            );
            let same = false;
            polyominoesT[polyominoName].forEach((pt) => {
                if (PUZZLEUTIL.model.arePolyominosSame(polyT, pt)) {
                    same = true;
                }
            });
            if (!same) {
                polyominoesT[polyominoName].push(polyT);
            }
        }
    });
    return polyominoesT;
};
PUZZLEUTIL.model.calcPolyominoesRotationAndFlip = (polyominoes) => {
    const polyominoesT = {};
    Object.entries(polyominoes).forEach(([polyominoName, polyomino]) => {
        polyominoesT[polyominoName] = [];
        for (let rotation = 0; rotation < 4; rotation += 1) {
            for (let flip = 0; flip <= 1; flip += 1) {
                const polyT = PUZZLEUTIL.model.translatePolyominoToOrigin(
                    PUZZLEUTIL.model.flipPolyomino(
                        PUZZLEUTIL.model.rotatePolyomino(polyomino, rotation), 
                        flip
                    )
                );
                let same = false;
                polyominoesT[polyominoName].forEach((pt) => {
                    if (PUZZLEUTIL.model.arePolyominosSame(polyT, pt)) {
                        same = true;
                    }
                });
                if (!same) {
                    polyominoesT[polyominoName].push(polyT);
                }
            }
        }
    });
    return polyominoesT;
};
PUZZLEUTIL.model.calcPolyominoBounds = (polyomino) => {
    const bounds = {
        row: {},
        column: {},
    };
    polyomino.forEach((p) => {
        const r = p[1];
        const c = p[0];
        if (bounds.row.min == undefined || r < bounds.row.min) {
            bounds.row.min = r;
        }
        if (bounds.row.max == undefined || r > bounds.row.max) {
            bounds.row.max = r;
        }
        if (bounds.column.min == undefined || c < bounds.column.min) {
            bounds.column.min = c;
        }
        if (bounds.column.max == undefined || c > bounds.column.max) {
            bounds.row.max = c;
        }
    });
    return bounds;
};
PUZZLEUTIL.model.translatePolyominoToOrigin = (polyomino) => {
    const bounds = PUZZLEUTIL.model.calcPolyominoBounds(polyomino);
    const polyominoT = [];
    polyomino.forEach((p) => {
        const pt = [p[0] - bounds.column.min, p[1] - bounds.row.min];
        polyominoT.push(pt);
    });
    return polyominoT;
};
PUZZLEUTIL.model.arePolyominosSame = (a, b) => {
    if (a.length != b.length) {
        return false;
    }
    const s = (i) => {
        const fix = (x) => x === -0 ? 0 : x;
        return `${fix(i[0])},${fix(i[1])}`;
    }
    const t = {};
    a.forEach((i) => {
        t[s(i)] = true;
    });
    let same = true;
    b.forEach((i) => {
        if (t[s(i)] == undefined) {
            same = false;
        }
    });
    return same;
};
PUZZLEUTIL.model.rotatePolyomino = (polyomino, rotationIndex) => {
    if (rotationIndex == 0) {
        return polyomino;
    }
    if (rotationIndex == 1) {
        const rotatedPolyomino = [];
        polyomino.forEach((s) => {
            rotatedPolyomino.push([-s[1], s[0]]);
        });
        return rotatedPolyomino;
    }
    if (rotationIndex == 2) {
        const rotatedPolyomino = [];
        polyomino.forEach((s) => {
            rotatedPolyomino.push([-s[0],-s[1]]);
        });
        return rotatedPolyomino;
    }
    if (rotationIndex == 3) {
        const rotatedPolyomino = [];
        polyomino.forEach((s) => {
            rotatedPolyomino.push([s[1], -s[0]]);
        });
        return rotatedPolyomino;
    }
    return null;
},
PUZZLEUTIL.model.flipPolyomino = (polyomino, flipIndex) => {
    if (flipIndex == 0) {
        return polyomino;
    }
    const flippedPolyomino = [];
    polyomino.forEach((s) => {
        flippedPolyomino.push([-s[0], s[1]]);
    });
    return flippedPolyomino;
};
PUZZLEUTIL.model.polyominoFromCells = (cells, rowNumberOfCell, columnNumberOfCell) => {
    const polyomino = [];
    Object.keys(cells).forEach(cell => {
        const p = [
            rowNumberOfCell[cell],
            columnNumberOfCell[cell]
        ];
        polyomino.push(p);
    });
    return polyomino;
};
PUZZLEUTIL.model.identifyPolyomino = (polyomino, polyominoesT) => {
    polyominoesT = polyominoesT ?? PUZZLEUTIL.model.polyominoesT;
    const polyomino0 = PUZZLEUTIL.model.translatePolyominoToOrigin(polyomino);
    const matches = [];
    Object.entries(polyominoesT).forEach(([polyname, polyTs]) => {
        polyTs.forEach((polyT, index) => {
            const same = PUZZLEUTIL.model.arePolyominosSame(polyomino0, polyT);
            if (same) {
                matches.push(polyname);
            }
        });
    });
    if (matches.length == 0) {
        return undefined;
    }
    console.assert(matches.length === 1);
    return matches[0];
};
PUZZLEUTIL.model.polyominoesT = PUZZLEUTIL.model.calcPolyominoesRotationAndFlip(PUZZLEUTIL.model.polyominoes);
PUZZLEUTIL.model.tetrominoesT = PUZZLEUTIL.model.calcPolyominoesRotation(PUZZLEUTIL.model.tetrominoes);
PUZZLEUTIL.model.calcPolyominoCells = (grid, r, c, polyomino) => {
    let ok = true;
    const cells = {};
    polyomino.forEach((p) => {
        const row  = r + p[1];
        const column = c + p[0];
        const cell = grid.cellInRowColumn(row, column);
        if (grid.cells[cell] === undefined) {
            ok = false;
        } else {
            cells[cell] = true;
        }
    });
    if (!ok) {
        return undefined;
    }
    return cells;
};
PUZZLEUTIL.model.calcRectangleCells = (grid, r, c, numRows, numColumns) => {
    let ok = true;
    const cells = {};
    for (let j = 0; j < numRows; ++j) {
        for (let i = 0; i < numColumns; ++i) {
            const cell = grid.cellInRowColumn(r + j, c + i);
            if (grid.cells[cell] === undefined) {
                ok = false;
            } else {
                cells[cell] = true;
            }
        }
    }
    if (!ok) {
        return undefined;
    }
    return cells;
};
PUZZLEUTIL.model.allRectangleDimensionsWithArea = (area) => {
    const dimensions = [];
    for (let i = 1; i <= area; i += 1) {
        const j = area / i;
        if (Number.isInteger(i) && Number.isInteger(j)) {
            dimensions.push([i, j]);
        }
    }
    return dimensions;
};
PUZZLEUTIL.model.stringifyCellStates = (cells, stateFromCell) => {
    const a = [];
    Object.keys(cells).forEach(cell => {
        const cellState = stateFromCell[cell];
        a.push(cellState);
    });
    return a.join("");
};
PUZZLEUTIL.model.unstringifyCellStates = (cells, string) => {
    const stateFromCell = {};
    Object.keys(cells).forEach((cell, index) => {
        const char = string[index];
        stateFromCell[cell] = char;
    });
    return stateFromCell;
};
PUZZLEUTIL.model.splitIntoSpans = (items, isSeparatorFn) => {
    const spans = [];
    let start = 0;
    for (let i = 0; i < items.length; ++i) {
        const item = items[i];
        const isLast = (i == items.length - 1);
        const isSeparator = isSeparatorFn(item);
        if (isSeparator || isLast) {
            if (start < i) {
                let end = i;
                if (isLast && !isSeparator) {
                    end = items.length;
                }
                spans.push([start, end - start]);
            }
            start = i + 1;
        }
    }
    if (start < items.length - 1) {
        spans.push([start, items.length - start]);
    }
    return spans;
};
PUZZLEUTIL.model.compareCellStatesToSolution = (cells, stateFromCell, solutionStateFromCell, undecidedStates) => {
    if (undecidedStates === undefined) { undecidedStates = {"_": true}; }
    const correctCells = {};
    const incorrectCells = {};
    const undecidedCells = {};
    Object.keys(cells).forEach(cell => {
        const s1 = stateFromCell[cell];
        const s2 = solutionStateFromCell[cell];
        if (undecidedStates[s1] !== undefined) {
            undecidedCells[cell] = true;
        } else if (s1 === s2) {
            correctCells[cell] = true;
        } else {
            incorrectCells[cell] = true;
        }
    });
    const getStatus = () => {
        const numIncorrect = Object.keys(incorrectCells).length;
        const numUndecided = Object.keys(undecidedCells).length;
        if (numIncorrect > 0) {
            return "error";
        } else if (numUndecided > 0) {
            return "ok";
        } else {
            return "solved";
        }
    };
    return { status: getStatus(), correctCells, incorrectCells, undecidedCells };
};