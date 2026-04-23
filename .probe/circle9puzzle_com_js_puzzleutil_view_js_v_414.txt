PUZZLEUTIL.view = {};
PUZZLEUTIL.view.createSvg = (width, height, scale) => {
    const minSizePercent = 0.5;
    const maxSizePercent = 1;
    const svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("width", width * scale);
    svg.setAttribute("height", height * scale);
    svg.style["min-width"] = `${width * scale * minSizePercent}px`;
    svg.style["min-height"] = `${height * scale * minSizePercent}px`;
    svg.style["max-width"] = `${width * scale * maxSizePercent}px`;
    svg.style["max-height"] = `${height * scale * maxSizePercent}px`;
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    svg.classList.add("shrinkable-svg");
    svg.style.userSelect = "none";
    svg.oncontextmenu = (ev) => { ev.preventDefault(); }
    return svg;
};
PUZZLEUTIL.view.createGrid = (svg, numRows, numColumns, cellSize, doThinLines, doThickLines, position, lineStyle_, thickLineStyle_) => {
    if (position === undefined) {
        position = [0, 0];
    }
    if (lineStyle_ === undefined) { lineStyle_ = ""; }
    if (thickLineStyle_ === undefined) { thickLineStyle_ = ""; }
    const lineStyle = "stroke: black; opacity: 20%; stroke-width: 1pt; stroke-linecap: round;" + lineStyle_;
    const cellStyle = "fill: transparent; stroke: none;";
    const thickLineStyle = "stroke: black; stroke-width: 2pt; stroke-linecap: round;" + thickLineStyle_;
    const gridX = position[0] + 2;
    const gridY = position[1] + 2;
    const grid = {numRows, numColumns, cellSize, position: [gridX, gridY]};
    grid.cells = {};
    { // cells
        const layer = document.createElementNS(SVG_NS, "g");
        layer.classList.add("no-browser-stuff");
        layer.style.cursor = "pointer";
        svg.appendChild(layer);
        for (let r = 0; r < numRows; r += 1) {
            for (let c = 0; c < numColumns; c += 1) {
                const cellId = `R${r + 1}C${c + 1}`;
                const e = document.createElementNS(SVG_NS, "rect");
                e.style = cellStyle;
                e.cellId = cellId;
                const x = gridX + cellSize * c;
                const y = gridY + cellSize * r;
                e.setAttribute("x", x - 0.5);
                e.setAttribute("y", y - 0.5);
                e.setAttribute("width", cellSize + 1);
                e.setAttribute("height", cellSize + 1);
                layer.appendChild(e);
                grid.cells[cellId] = {
                    id: cellId, 
                    e, 
                    center: [x + cellSize / 2, y + cellSize / 2],
                    left: x,
                    right: x + cellSize,
                    top: y,
                    bottom: y + cellSize,
                    width: cellSize,
                    height: cellSize
                };
            }
        }
    }
    if (doThinLines) { // lines    
        const layer = document.createElementNS(SVG_NS, "g");
        svg.appendChild(layer);
        for (let r = 0; r <= numRows; ++r) {
            const e = document.createElementNS(SVG_NS, "line");
            const y = gridY + r * cellSize;
            e.setAttribute("x1", gridX);
            e.setAttribute("y1", y);
            e.setAttribute("x2", gridX + cellSize * numColumns);
            e.setAttribute("y2", y);
            e.style = lineStyle;
            e.style.pointerEvents = "none";
            layer.appendChild(e);
        }
        for (let c = 0; c <= numColumns; ++c) {
            const e = document.createElementNS(SVG_NS, "line");
            const x = gridX + c * cellSize;
            e.setAttribute("x1", x);
            e.setAttribute("y1", gridY);
            e.setAttribute("x2", x);
            e.setAttribute("y2", gridY + cellSize * numRows);
            e.style = lineStyle;
            e.style.pointerEvents = "none";
            layer.appendChild(e);
        }
    }
    if (doThickLines) {
        const isOutsideEdge = (cell1, cell2) => (cell1 === undefined) !== (cell2 === undefined); 
        // const edges2 = PUZZLEUTIL.view.createEdges(svg, grid, "stroke: #aaa; stroke-width: 4pt; stroke-linecap: round;");
        const edges1 = PUZZLEUTIL.view.createEdges(svg, grid, "stroke: black; stroke-width: 2pt; stroke-linecap: round;");
        [edges1/*, edges2*/].forEach(edges => {
            PUZZLEUTIL.view.refreshEdges(svg, edges, isOutsideEdge);
        });
        grid.edges1 = edges1;
        // grid.edges2 = edges2;
    }
    // if (doThickLines) { // thick lines
    //     const layer = document.createElementNS(SVG_NS, "g");
    //     svg.appendChild(layer);
    //     const makeThickLineHorizontal = (r, c) => {
    //         const e = document.createElementNS(SVG_NS, "line");
    //         const x = gridX + (c - 1) * cellSize;
    //         const y = gridY + (r - 1) * cellSize;
    //         e.setAttribute("x1", x);
    //         e.setAttribute("y1", y);
    //         e.setAttribute("x2", x + cellSize);
    //         e.setAttribute("y2", y);
    //         e.style = thickLineStyle;
    //         e.style.pointerEvents = "none";
    //         layer.appendChild(e);
    //     };
    //     const makeThickLineVertical = (r, c) => {
    //         const e = document.createElementNS(SVG_NS, "line");
    //         const x = gridX + (c - 1) * cellSize;
    //         const y = gridY + (r - 1) * cellSize;
    //         e.setAttribute("x1", x);
    //         e.setAttribute("y1", y);
    //         e.setAttribute("x2", x);
    //         e.setAttribute("y2", y + cellSize);
    //         e.style = thickLineStyle;
    //         e.style.pointerEvents = "none";
    //         layer.appendChild(e);
    //     };
    //     for (let r = 1; r <= numRows; r += 1) {
    //         makeThickLineVertical(r, 1);
    //         makeThickLineVertical(r, numColumns + 1);
    //     }
    //     for (let c = 1; c <= numColumns; c += 1) {
    //         makeThickLineHorizontal(1, c);
    //         makeThickLineHorizontal(numRows + 1, c);
    //     }
    // }

    return grid;
};
PUZZLEUTIL.view.createText = (svg, grid, style) => {
    const numbers = {};
    const layer = document.createElementNS(SVG_NS, "g");
    Object.keys(grid.cells).forEach((cellId) => {
        const gridCell = grid.cells[cellId];
        const e = document.createElementNS(SVG_NS, "text");
        e.setAttribute("x", gridCell.center[0]);
        e.setAttribute("y", gridCell.center[1]);
        e.style = "font-weight: normal; fill: black; stroke: none; text-anchor: middle; dominant-baseline: central; font-size: 25px;" + style;
        e.style.pointerEvents = "none";
        layer.appendChild(e);
        numbers[cellId] = e;
    });
    svg.appendChild(layer);
    return numbers;
};
PUZZLEUTIL.view.createTextCorner = (svg, grid, style) => {
    const numbers = {};
    const layer = document.createElementNS(SVG_NS, "g");
    Object.keys(grid.cells).forEach((cellId) => {
        const gridCell = grid.cells[cellId];
        const e = document.createElementNS(SVG_NS, "text");
        e.setAttribute("x", gridCell.center[0] - grid.cellSize * 0.32);
        e.setAttribute("y", gridCell.center[1] - grid.cellSize * 0.26);
        e.style = "font-weight: normal; fill: black; stroke: none; text-anchor: middle; dominant-baseline: central; font-size: 12pt;" + style;
        e.style.pointerEvents = "none";
        layer.appendChild(e);
        numbers[cellId] = e;
    });
    svg.appendChild(layer);
    return numbers;
};
PUZZLEUTIL.view.createEdges = (svg, grid, style) => {
    const layer = document.createElementNS(SVG_NS, "g");
    svg.appendChild(layer);
    return {layer, grid, style};
};
PUZZLEUTIL.view.refreshEdgesSlow = (svg, edges, isEdgeBetweenCells) => {
    const lineStyle = " stroke: black; stroke-width: 1pt; stroke-linecap: round; " + edges.style;
    edges.layer.innerHTML = "";
    const cellInRowColumn = (r, c) => {
        if (r < 0 || c < 0 || r >= edges.grid.numRows || c >= edges.grid.numColumns) {
            return undefined;
        }
        return `R${r + 1}C${c + 1}`;
    };
    for (let r = -1; r < edges.grid.numRows; r += 1) {
        for (let c = 0; c < edges.grid.numColumns; c += 1) {
            const cell1 = cellInRowColumn(r, c);
            const cell2 = cellInRowColumn(r + 1, c);
            let isEdge = isEdgeBetweenCells(cell1, cell2);
            let style = "";
            if (typeof(isEdge) !== "boolean") {
                style = isEdge[1];
                isEdge = isEdge[0];
            }
            if (isEdge) {
                const line = document.createElementNS(SVG_NS, "line");
                const x1 = edges.grid.position[0] + edges.grid.cellSize * c;
                const x2 = edges.grid.position[0] + edges.grid.cellSize * (c + 1);
                const y1 = edges.grid.position[1] + edges.grid.cellSize * (r + 1);
                const y2 = y1;
                line.setAttribute("x1", x1);
                line.setAttribute("y1", y1);
                line.setAttribute("x2", x2);
                line.setAttribute("y2", y2);
                line.style = `${lineStyle}${style}`;
                line.style.pointerEvents = "none";
                edges.layer.appendChild(line);
            }
        }
    }
    for (let r = 0; r < edges.grid.numRows; r += 1) {
        for (let c = -1; c < edges.grid.numColumns; c += 1) {
            const cell1 = cellInRowColumn(r, c);
            const cell2 = cellInRowColumn(r, c + 1);
            let isEdge = isEdgeBetweenCells(cell1, cell2);
            let style = "";
            if (typeof(isEdge) !== "boolean") {
                style = isEdge[1];
                isEdge = isEdge[0];
            }
            if (isEdge) {
                const line = document.createElementNS(SVG_NS, "line");
                const y1 = edges.grid.position[1] + edges.grid.cellSize * r;
                const y2 = edges.grid.position[1] + edges.grid.cellSize * (r + 1);
                const x1 = edges.grid.position[0] + edges.grid.cellSize * (c + 1);
                const x2 = x1;
                line.setAttribute("x1", x1);
                line.setAttribute("y1", y1);
                line.setAttribute("x2", x2);
                line.setAttribute("y2", y2);
                line.style = `${lineStyle}${style}`;
                line.style.pointerEvents = "none";
                edges.layer.appendChild(line);
            }
        }
    }
};
PUZZLEUTIL.view.refreshEdges = (svg, edges, isEdgeBetweenCells) => {
    const lineStyle = " pointer-events: none; stroke: black; stroke-width: 1pt; stroke-linecap: round; " + edges.style;
    edges.layer.innerHTML = "";
    const cellInRowColumn = (r, c) => {
        if (r < 0 || c < 0 || r >= edges.grid.numRows || c >= edges.grid.numColumns) {
            return undefined;
        }
        return `R${r + 1}C${c + 1}`;
    };
    const path = [];
    for (let r = -1; r < edges.grid.numRows; r += 1) {
        for (let c = 0; c < edges.grid.numColumns; c += 1) {
            const cell1 = cellInRowColumn(r, c);
            const cell2 = cellInRowColumn(r + 1, c);
            let isEdge = isEdgeBetweenCells(cell1, cell2);
            let style = "";
            if (typeof(isEdge) !== "boolean") {
                console.error();
            }
            if (isEdge) {
                const line = document.createElementNS(SVG_NS, "line");
                const x1 = edges.grid.position[0] + edges.grid.cellSize * c;
                const x2 = edges.grid.position[0] + edges.grid.cellSize * (c + 1);
                const y1 = edges.grid.position[1] + edges.grid.cellSize * (r + 1);
                const y2 = y1;
                path.push(`M${x1},${y1} L${x2},${y2}`);
            }
        }
    }
    for (let r = 0; r < edges.grid.numRows; r += 1) {
        for (let c = -1; c < edges.grid.numColumns; c += 1) {
            const cell1 = cellInRowColumn(r, c);
            const cell2 = cellInRowColumn(r, c + 1);
            let isEdge = isEdgeBetweenCells(cell1, cell2);
            let style = "";
            if (typeof(isEdge) !== "boolean") {
                console.error();
            }
            if (isEdge) {
                const line = document.createElementNS(SVG_NS, "line");
                const y1 = edges.grid.position[1] + edges.grid.cellSize * r;
                const y2 = edges.grid.position[1] + edges.grid.cellSize * (r + 1);
                const x1 = edges.grid.position[0] + edges.grid.cellSize * (c + 1);
                const x2 = x1;
                path.push(`M${x1},${y1} L${x2},${y2}`);
            }
        }
    }
    const pathStr = path.join(" ");
    const pathEl = createEl({
        tag: "path",
        d: pathStr,
    });
    pathEl.style = lineStyle;
    edges.layer.appendChild(pathEl);
};
PUZZLEUTIL.view.createCircles = (svg, grid, radius, style) => {
    const circles = {};
    const layer = document.createElementNS(SVG_NS, "g");
    Object.keys(grid.cells).forEach(cell => {
        const gridCell = grid.cells[cell];
        const e = document.createElementNS(SVG_NS, "circle");
        e.style = style;
        e.setAttribute("cx", gridCell.center[0]);
        e.setAttribute("cy", gridCell.center[1]);
        e.setAttribute("r", radius);
        e.style.pointerEvents = "none";
        layer.appendChild(e);
        circles[cell] = e;
    });
    svg.appendChild(layer);
    return { layer, circles };
};
PUZZLEUTIL.view.createRects = (svg, grid, style_) => {
    if (style_ === undefined) { style_ = ""; }
    const style = "fill: black; stroke: none; " + style_;
    const rectFromCell = {};
    const g = document.createElementNS(SVG_NS, "g");
    Object.keys(grid.cells).forEach(cell => {
        const gridCell = grid.cells[cell];
        const e = document.createElementNS(SVG_NS, "rect");
        e.style = style;
        e.setAttribute("x", gridCell.center[0] - gridCell.width/2-1);
        e.setAttribute("y", gridCell.center[1] - gridCell.height/2-1);
        e.setAttribute("width", gridCell.width+2);
        e.setAttribute("height", gridCell.height+2);
        g.appendChild(e);
        rectFromCell[cell] = e;
    });
    svg.appendChild(g);
    return {g, rectFromCell};
};
PUZZLEUTIL.view.setPointerDownDragUpListeners = (element, onDown, onDragMove, onUp) => {
    function onDragMoveWrap(event) {
        event.preventDefault();
        const realTarget = document.elementFromPoint(event.clientX, event.clientY);
        if (!realTarget) { return; }
        event.realTarget = realTarget;
        onDragMove(event);
    }
    function onUpWrap(event) {
        event.preventDefault();
        window.removeEventListener("pointermove", onDragMoveWrap);
        // window.removeEventListener("touchmove", onDragMoveWrap);
        window.removeEventListener("pointerup", onUpWrap);
        window.removeEventListener("blur", onUpWrap);  
        onUp(event);
    }
    const setEventListeners = (target) => {
        const h = (event) => {
            event.preventDefault();
            event.realTarget = event.target;
            onDown(event);
            window.addEventListener("pointermove", onDragMoveWrap);
            // window.addEventListener("touchmove", onDragMoveWrap);
            window.addEventListener("pointerup", onUpWrap);  
            window.addEventListener("blur", onUpWrap);  
        };
        target.addEventListener("pointerdown", h);
        target.addEventListener("touchstart", (event) => {event.preventDefault(); });
        // target.addEventListener("touch", (event) => {
        //     onDown(event);
        //     onUp(event);
        // });
        target.addEventListener("contextmenu", (event) => { event.preventDefault(); });
    };
    setEventListeners(element);
};
PUZZLEUTIL.view.setGridDownDragUpListeners = (grid, onDown, onDragMove, onUp) => {
    Object.keys(grid.cells).forEach(cell => {
        const element = grid.cells[cell].e;
        element.cell = cell; // TODO:jkd custom property on element
        PUZZLEUTIL.view.setPointerDownDragUpListeners(element, onDown, onDragMove, onUp);
    });
};
PUZZLEUTIL.view.setGridDownDragUpListenersToCycleCellState = (view, grid, cellStateCycle, noninteractiveFromCell) => {
    let interaction = null;
    // const reverseCellStateCycle = reverseArray(cellStateCycle);
    const onDown = (ev) => {
        const cell = ev.target.cell;
        if (!cell) { return; }
        if (noninteractiveFromCell[cell] != null) { 
            let ni = noninteractiveFromCell[cell];
            if (ni === true) { return; }
            if (typeof ni === 'function') {
                ni(cell);
                return;
            }
        }
        const s1 = view.state.cells[cell];
        const s2 = cycleBetween(
            s1, 
            cellStateCycle
            // ev.button == 2 ? reverseCellStateCycle : cellStateCycle
        );
        const command = [cell, s1, s2];
        view.hooks.doCommandAndWriteToHistory(view, command);
        interaction = { setStateFrom: s1, setStateTo: s2 };
    };
    const onDragMove = (ev) => {
        const cell = ev.realTarget.cell;
        if (!interaction) { return; }
        if (!cell) { return; }
        if (noninteractiveFromCell[cell]) { return; }
        const s1 = view.state.cells[cell];
        const s2 = interaction.setStateTo;
        const command = [cell, s1, s2];
        if (s1 !== s2) {
            // if (s1 === '_' || s1 === interaction.setStateFrom) {
                view.hooks.doCommandAndWriteToHistory(view, command);
            // }
        }
    };
    const onUp = (ev) => {
        interaction = null;
    };
    PUZZLEUTIL.view.setGridDownDragUpListeners(grid, onDown, onDragMove, onUp);
    return { endInteraction: onUp };
};
PUZZLEUTIL.view.setDownDragUpListenersToTilePlacement = (genre, view, noninteractiveFromTile, onSelect) => {
    const snap = (event) => {
        const snap1 = () => {
            const overElements = document.elementsFromPoint(event.clientX, event.clientY);
            for (let i = 0; i < overElements.length; ++i) {
                const overE = overElements[i];
                if (overE.location !== undefined) {
                    return overE;
                }
            }
            return undefined;
        };
        const e = snap1();
        if (e === undefined) { return undefined; }
        const location = e.location;
        const tile = view.state.tileFromLocation[location];
        if (tile !== undefined && tile !== view.selectedTile) { return undefined; }
        return e;
    };
    let interaction = undefined;
    const onDownCell = (event) => {
        const location = event.target.location;
        if (location === undefined) { return; }
        if (view.selectedTile === undefined) { return; }
        const isLocationEmpty = view.state.tileFromLocation[location] === undefined;
        if (!isLocationEmpty) { return; }
        const tile = view.selectedTile;
        if (noninteractiveFromTile[tile] !== undefined) { return; }
        const fromLocation = view.state.locationFromTile[tile];
        const toLocation = location;
        const command = genre.makeCommand(view.model, view.state, tile, fromLocation, toLocation);
        if (command !== undefined) {
            view.hooks.doCommandAndWriteToHistory(view, command);
        }
        view.selectedTile = undefined;
        interaction = undefined;
        genre.refreshView(view);
        return;
    };
    const onDownTile = (event) => {
        const tileE = event.target;
        if (tileE === undefined) { return; }
        const tile = tileE.tile;
        if (tile === undefined) { return; }
        if (noninteractiveFromTile[tile] !== undefined) { return; }
        if (interaction !== undefined && interaction.tile === tile) {
            interaction = undefined;
            view.selectedTile = undefined;
            onSelect();
            genre.refreshView(view);
            return;
        }
        const tileG = tileE.parentElement;
        const [tileX, tileY] = getElementTransformTranslate(tileG);
        const [svgX, svgY] = clientPointToSVG(event.clientX, event.clientY, tileG.ownerSVGElement);
        const offsetX = svgX - tileX;
        const offsetY = svgY - tileY;
        interaction = {tile, tileE, tileG, offsetX, offsetY, sticky: true};
        view.selectedTile = tile;
        onSelect();
        genre.refreshView(view);
    };
    const onDragMoveTile = (event) => {
        if (interaction === undefined) { return; }
        const tileG = interaction.tileG;
        const snapToE = snap(event);
        if (snapToE !== undefined) {
            const snapX = snapToE.getAttribute("x");
            const snapY = snapToE.getAttribute("y");
            const x = snapX;
            const y = snapY;
            tileG.setAttribute("transform", `translate(${x},${y})`);
            const location = snapToE.location;
            if (location.toString() !== view.state.locationFromTile[interaction.tile].toString()) {
                interaction.sticky = false;
            }
        } else {
            const [x, y] = clientPointToSVG(event.clientX, event.clientY, tileG.ownerSVGElement);
            tileG.setAttribute("transform", `translate(${x - interaction.offsetX},${y - interaction.offsetY})`);
            interaction.sticky = false;
        }
    };
    const onUpTile = (event) => {
        if (interaction === undefined) { return; }
        if (interaction.sticky === false) {
            const snapToE = snap(event);
            if (snapToE !== undefined) {
                const tile = interaction.tile;
                const fromLocation = view.state.locationFromTile[tile];
                const toLocation = snapToE.location;
                const command = genre.makeCommand(view.model, view.state, tile, fromLocation, toLocation);
                if (command !== undefined) {
                    view.hooks.doCommandAndWriteToHistory(view, command);
                }
            }
            view.selectedTile = undefined;
        }
        interaction = undefined;
        genre.refreshView(view);
    };
    Object.entries(view.cellRectEFromLocation).forEach(([location, rectE]) => {
        rectE.location = location.split(","); // TODO:jkd custom property on element
        rectE.onpointerdown = onDownCell;
    });
    Object.entries(view.rectEFromTile).forEach(([tile, tileRectE]) => {
        tileRectE.tile = tile; // TODO:jkd custom property on element
        PUZZLEUTIL.view.setPointerDownDragUpListeners(tileRectE, onDownTile, onDragMoveTile, onUpTile);
    });
}
PUZZLEUTIL.view.setDefaultSettings = (view, settings) => {
    view.settingsValues = {};
    settings.forEach(setting => {
        view.settingsValues[setting.id] = setting.defaultValue;
    });
};
PUZZLEUTIL.view.createAnimator = (onCompleteAll) => {
    const animator = {
        handle: undefined,
        previousTimestamp: undefined,
        animations: [],
        onCompleteAll
    };
    animator.play = (duration, fn, id, overlap) => {
        animator.playKeyframes([{duration, fn}], id, overlap);
    };
    const skipRestOfAnim = (anim) => {
        const lastKeyframe = anim.keyframes[anim.keyframes.length - 1];
        if (lastKeyframe === undefined) {
            return;
        }
        lastKeyframe.fn(1);
    };
    animator.stopAll = (withTag) => {
        animator.animations.forEach(anim => {
            if (withTag === undefined || anim.tag === withTag) {
                skipRestOfAnim(anim);
                anim.remove = true;
            }
        });
        animator.animations = animator.animations.filter(a => undefined === a.remove);
    };
    animator.playKeyframes = (keyframes, id, overlap, tag) => {
        if (overlap === undefined) { overlap = "truncate"; };
        const duration = keyframes.reduce((duration, keyframe) => keyframe.duration + duration, 0);
        const anim = {keyframes, id, tag, elapsed: 0, duration};
        if (id !== undefined) {
            const animations = [];
            let didAppend = false;
            animator.animations.forEach(otherAnim => {
                if (otherAnim.id === id) {
                    if (overlap === "truncate") {
                        skipRestOfAnim(otherAnim);
                    } else if (overlap === "append") {
                        otherAnim.keyframes = otherAnim.keyframes.concat(keyframes);
                        otherAnim.duration += duration;
                        animations.push(otherAnim);
                        didAppend = true;
                    } else if (overlap === "stack") {
                        animations.push(otherAnim);
                    } else {
                        throw new Error(`unrecognized overlap: ${overlap}`);
                    }
                } else {
                    animations.push(otherAnim);
                }
            });
            if (!didAppend) {
                animations.push(anim);
            }
            animator.animations = animations;
        }
        animator.resume();
    };
    const findKeyframeAtTime = (keyframes, elapsed) => {
        let total = 0;
        for (let i = 0; i < keyframes.length; ++i) {
            const keyframe = keyframes[i];
            if (total + keyframe.duration > elapsed) {
                let t = (elapsed - total) / keyframe.duration;
                if (t < 0) { t = 0; }
                if (t > 1) { t = 1; }
                return {index: i, t};
            }
            total += keyframe.duration;
        }
        return {index: keyframes.length - 1, t: 1};
    };
    const animationFrameCallback = (timestamp) => {
        if (animator.previousTimestamp === undefined) {
            animator.previousTimestamp = timestamp;
        }
        // console.log(animator.animations.length);
        const maxElapsed = 100;
        const dTimestamp = timestamp - animator.previousTimestamp;
        const animatorTimeScale = 1;
        const elapsed = animatorTimeScale * Math.min(maxElapsed, dTimestamp);
        animator.animations.forEach(anim => {
            anim.elapsed += elapsed;
            const f = findKeyframeAtTime(anim.keyframes, anim.elapsed);
            const keyframe = anim.keyframes[f.index];
            keyframe.fn(f.t);
        });
        animator.previousTimestamp = timestamp;
        animator.animations = animator.animations.filter(anim => anim.elapsed < anim.duration);
        if (animator.animations.length > 0) {
            animator.handle = requestAnimationFrame(animationFrameCallback);
        } else {
            animator.previousTimestamp = undefined;
            animator.handle = undefined;
            if (animator.onCompleteAll) {
                animator.onCompleteAll();
            }
        }
    };
    animator.resume = () => {
        if (animator.handle === undefined) {
            animator.handle = requestAnimationFrame(animationFrameCallback);
        }
    }
    return animator;
};
const setClickRepeatHandler = (element, handler) => {
    const delay = 400;
    const period = 100;
    let delayId;
    let repeatId;
    const end = () => {
        if (delayId !== undefined) {
            clearTimeout(delayId);
            delayId = undefined;
        }
        if (repeatId !== undefined) {
            clearInterval(repeatId);
            repeatId = undefined;
        }
        window.removeEventListener("pointerup", end);
        element.classList.remove("active");
    };
    element.onpointerdown = (ev) => {
        element.classList.add("active");
        ev.preventDefault();
        handler();
        delayId = setTimeout(() => {
            repeatId = setInterval(handler, period);
        }, delay);
        window.addEventListener("pointerup", end);
    };
    element.onclick = (ev) => {
        ev.preventDefault();
    };
};
PUZZLEUTIL.view.refreshEdgesInset = (grid, gridView, g, selectedFromCell, primarySelectedCell, color) => {
    g.innerHTML = "";
    const edgesFromCell = {};
    Object.keys(grid.cells).forEach(cell => {
        const cellLeft = grid.neighborOfCell[cell]["left"];
        const cellRight = grid.neighborOfCell[cell]["right"];
        const cellUp = grid.neighborOfCell[cell]["up"];
        const cellDown = grid.neighborOfCell[cell]["down"];
        const selected = selectedFromCell[cell] !== undefined;
        const selectedLeft = selectedFromCell[cellLeft] !== undefined;
        const selectedRight = selectedFromCell[cellRight] !== undefined;
        const selectedUp = selectedFromCell[cellUp] !== undefined;
        const selectedDown = selectedFromCell[cellDown] !== undefined;
        edgesFromCell[cell] = {
            up: selected && !selectedUp,
            down: selected && !selectedDown,
            left: selected && !selectedLeft,
            right: selected && !selectedRight,
        };
    });
    const inset = 3;
    const style = `stroke: ${color}; stroke-width: 4pt; stroke-linecap: square;`;
    const rectColorSelectedPrimary = "#cef";
    const rectColorSelected = rectColorSelectedPrimary;
    const rectColorNotSelected = "white";
    for (let r = 1; r <= grid.numRows; ++r) {
        for (let c = 1; c <= grid.numColumns - 1; ++c) {
            const cell1 = grid.cellInRowColumn(r, c + 0);
            if (selectedFromCell[cell1] === undefined) { continue; }
            const cell2 = grid.cellInRowColumn(r, c + 1);
            const cell3 = grid.cellInRowColumn(r - 1, c + 1);
            const cell4 = grid.cellInRowColumn(r + 1, c + 1);
            const isEdge1 = edgesFromCell[cell1] || {};
            const isEdge2 = edgesFromCell[cell2] || {};
            const isEdge3 = edgesFromCell[cell3] || {};
            const isEdge4 = edgesFromCell[cell4] || {};
            const cellInfo1 = gridView.cells[cell1];
            const cellInfo2 = gridView.cells[cell2];
            if (!isEdge1["right"]) {
                if (isEdge2["up"] || isEdge3["left"]) {
                    const line = document.createElementNS(SVG_NS, "line");
                    line.setAttribute("y1", cellInfo1.top + inset);
                    line.setAttribute("y2", cellInfo2.top + inset);
                    line.setAttribute("x1", cellInfo1.right - inset);
                    line.setAttribute("x2", cellInfo2.left + inset);
                    line.style = style;
                    g.appendChild(line);
                }
                if (isEdge2["down"] || isEdge4["left"]) {
                    const line = document.createElementNS(SVG_NS, "line");
                    line.setAttribute("y1", cellInfo1.bottom - inset);
                    line.setAttribute("y2", cellInfo2.bottom - inset);
                    line.setAttribute("x1", cellInfo1.right - inset);
                    line.setAttribute("x2", cellInfo2.left + inset);
                    line.style = style;
                    g.appendChild(line);
                }
            }
        }
    }
    for (let r = 1; r <= grid.numRows - 1; ++r) {
        for (let c = 1; c <= grid.numColumns; ++c) {
            const cell1 = grid.cellInRowColumn(r + 0, c);
            if (selectedFromCell[cell1] === undefined) { continue; }
            const cell2 = grid.cellInRowColumn(r + 1, c);
            const cell3 = grid.cellInRowColumn(r + 1, c - 1);
            const cell4 = grid.cellInRowColumn(r + 1, c + 1);
            const isEdge1 = edgesFromCell[cell1] || {};
            const isEdge2 = edgesFromCell[cell2] || {};
            const isEdge3 = edgesFromCell[cell3] || {};
            const isEdge4 = edgesFromCell[cell4] || {};
            const cellInfo1 = gridView.cells[cell1];
            const cellInfo2 = gridView.cells[cell2];
            if (!isEdge1["down"]) {
                if (isEdge2["left"] || isEdge3["up"]) {
                    const line = document.createElementNS(SVG_NS, "line");
                    line.setAttribute("x1", cellInfo1.left + inset);
                    line.setAttribute("x2", cellInfo2.left + inset);
                    line.setAttribute("y1", cellInfo1.bottom - inset);
                    line.setAttribute("y2", cellInfo2.top + inset);
                    line.style = style;
                    g.appendChild(line);
                }
                if (isEdge2["right"] || isEdge4["up"]) {
                    const line = document.createElementNS(SVG_NS, "line");
                    line.setAttribute("x1", cellInfo1.right - inset);
                    line.setAttribute("x2", cellInfo2.right - inset);
                    line.setAttribute("y1", cellInfo1.bottom - inset);
                    line.setAttribute("y2", cellInfo2.top + inset);
                    line.style = style;
                    g.appendChild(line);
                }
            }
        }
    }
    Object.keys(grid.cells).forEach(cell => {
        const selectedPrimary = cell === primarySelectedCell;
        const selected = selectedFromCell[cell] !== undefined;
        const cellInfo = gridView.cells[cell];
        const rect = cellInfo.e;
        rect.style.fill = selectedPrimary ? rectColorSelectedPrimary : selected ? rectColorSelected : rectColorNotSelected;
        const isEdge = edgesFromCell[cell];
        if (isEdge["up"]) {
            const line = document.createElementNS(SVG_NS, "line");
            line.setAttribute("y1", cellInfo.top + inset);
            line.setAttribute("y2", cellInfo.top + inset);
            line.setAttribute("x1", cellInfo.left + inset);
            line.setAttribute("x2", cellInfo.left + cellInfo.width - inset);
            line.style = style;
            g.appendChild(line);
        }
        if (isEdge["down"]) {
            const line = document.createElementNS(SVG_NS, "line");
            line.setAttribute("y1", cellInfo.bottom - inset);
            line.setAttribute("y2", cellInfo.bottom - inset);
            line.setAttribute("x1", cellInfo.left + inset);
            line.setAttribute("x2", cellInfo.left + cellInfo.width - inset);
            line.style = style;
            g.appendChild(line);
        }
        if (isEdge["left"]) {
            const line = document.createElementNS(SVG_NS, "line");
            line.setAttribute("x1", cellInfo.left + inset);
            line.setAttribute("x2", cellInfo.left + inset);
            line.setAttribute("y1", cellInfo.top + inset);
            line.setAttribute("y2", cellInfo.top + cellInfo.height - inset);
            line.style = style;
            g.appendChild(line);
        }
        if (isEdge["right"]) {
            const line = document.createElementNS(SVG_NS, "line");
            line.setAttribute("x1", cellInfo.right - inset);
            line.setAttribute("x2", cellInfo.right - inset);
            line.setAttribute("y1", cellInfo.top + inset);
            line.setAttribute("y2", cellInfo.top + cellInfo.height - inset);
            line.style = style;
            g.appendChild(line);
        }
    });
};