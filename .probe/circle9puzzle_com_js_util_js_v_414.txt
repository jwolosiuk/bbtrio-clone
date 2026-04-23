// Copyright 2023 James Dewar. All rights reserved.
"use strict";
const SVG_NS = "http://www.w3.org/2000/svg";
const XLINK_NS = "http://www.w3.org/1999/xlink";
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = (hash * 31 + str.charCodeAt(i)) >>> 0;
    }
    return hash.toString(16);
}
const shallowCopyObject = (object) => {
    const copy = {};
    Object.entries(object).forEach(([key, value]) => {
        copy[key] = value;
    });
    return copy;
};
const shallowCopyObjectInto = (from, to) => {
    Object.keys(from).forEach(key => {
        to[key] = from[key];
    });
};
const shallowCopyArray = (array) => {
    return array.map((value) => value);
};
const shuffleArray = (arrayIn) => {
    let array = [];
    for (let i = 0; i < arrayIn.length; ++i) {
        array.push(arrayIn[i]);
    }
    for (let i = array.length - 1; i > 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
};
const randomArrayElement = (array) => {
    const i = Math.floor(Math.random() * array.length);
    return array[i];
};
const arrayWithItemRemoved = (array, item) => {
    return array.filter(it => it !== item);
};
const clearArray = (array) => {
    while (array.length > 0) { array.pop(); }
};
const firstArrayElement = (array) => {
    return array[0];
};
const lastArrayElement = (array) => {
    return array[array.length - 1];
};
const reverseArray = (array) => {
    const r = [];
    for (let i = array.length - 1; i >= 0; --i) {
        r.push(array[i]);
    }
    return r;
}
const integersInclusive = (from, to, step) => {
    step = step ?? 1;
    const r = [];
    for (let i = from; i <= to; i += step) {
        r.push(i);
    }
    return r;
};
const integersExclusive = (from, to, step) => {
    step = step ?? 1;
    const r = [];
    for (let i = from; i < to; i += step) {
        r.push(i);
    }
    return r;
};
const integers = integersInclusive;
const integersInc = integersInclusive;
const integersExc = integersExclusive;
const randomIntegerInclusive = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1) + min);
};
const mapObject = (o, callback) => {
    const r = {};
    Object.entries(o).forEach(([k, v]) => {
        r[k] = callback(k, v);
    });
    return r;
};
const objectFromSet = (set) => {
    const a = Array.from(set);
    const t = {};
    a.forEach(i => {
        t[i] = true;
    });
    return t;
};
const setOFromA = (a) => {
    const r = {};
    a.forEach(i => {r[i] = true; });
    return r;
};
const unionSetsO = (a, b) => {
    return setOFromA(Object.keys(a).concat(Object.keys(b)));
};
const intersectSetsO = (a, b) => {
    const ra = Object.keys(a).filter(i => b[i] !== undefined);
    return setOFromA(ra);
};
const createEnum = (strings) => {
    return Object.freeze(
        strings.reduce(
            (acc, str, index) => {
                acc[str] = index;
                acc[index] = str;
                return acc;
            }, 
            {}
        )
    );
};
const removeElement = (el) => {
    el.parentElement.removeChild(el);
};
const removeAllChildElements = (e) => {
    e.innerHTML = "";
};
const addOrRemoveClass = (e, class_, add) => {
    if (add) {
        e.classList.add(class_);
    } else {
        e.classList.remove(class_);
    }
};
const toggleClass = (e, class_) => {
    if (e.classList.contains(class_)) {
        e.classList.remove(class_);
    } else {
        e.classList.add(class_);
    }
};
const downloadContent = (content, fileName, contentType) => {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
};
const handlePortraitOrLandscape = (width, height) => {
    // XXX:jkd is this needed?
    const isPortrait = () => {
        if (typeof(window.orientation) == "number") {
            if (window.orientation == -90 || window.orientation == 90) {
                return false;
            }
            return true;
        } else {
            return screen.width < screen.height;
        }
    };
    const viewport = document.querySelector('meta[name="viewport"]');
    // const rest = ",user-scalable=no";
    const rest = ",user-scalable=yes";
    if (isPortrait()) {
        viewport.content = `width=${width}${rest}`;
    } else {
        viewport.content = `height=${height}${rest}`;
    }
    window.addEventListener("orientationchange", () => {
        handlePortraitOrLandscape(width, height);
    });
};
const replaceStringCharAt = (s, index, replacement) => {
    return s.substring(0, index) + replacement + s.substring(index + replacement.length);
};
const capitalizeFirstLetter = (s) => {
    if (s.length < 1) { return s; }
    return s[0].toUpperCase() + s.slice(1);
};
const reverseString = (s) => {
    return s.split("").reverse().join("");
};
const escapeRegExp = (str) => {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
};
const cycleBetween = (current, list_, reverse = false) => {
    const list = reverse === true ? shallowCopyArray(list_).reverse() : list_;
    for (let i = 0; i < list.length; i += 1) {
        const j = i == list.length - 1 ? 0 : i + 1;
        if (current === list[i]) {
            return list[j];
        }
    }
    return list[0];
};
const cycleArray = (array, n) => {
    if (array.length === 0) {
        return undefined;
    }
    const index = Math.abs(n) % array.length;
    return array[index];
};
const msToTimeString = (totalMs) => {
    let t = totalMs;
    const hours = Math.floor(t / 1000 / 60 / 60);
    t -= hours * 1000 * 60 * 60;
    const minutes = Math.floor(t / 1000 / 60);
    t -= minutes * 1000 * 60;
    const seconds = Math.floor(t / 1000);
    t -= seconds * 1000;
    const milliseconds = t;

    const secondsS = ('00'+seconds).slice(-2);
    if (hours > 0) {
        const hoursS = `${hours}`;
        const minutesS = ('00'+minutes).slice(-2);
        return `${hoursS}:${minutesS}:${secondsS}`;
    } else {
        const minutesS = `${minutes}`;
        return `${minutesS}:${secondsS}`;
    }
};
const lerp = (from, to, t) => from + (to - from) * t;
const lerpArray = (from, to, t) => {
    const r = [];
    const len = Math.max(from.length, to.length);
    for (let i = 0; i < len; ++i) {
        const a = from[i];
        const b = to[i];
        if (a === undefined && b === undefined) {
            r.push(undefined);
        } else if (a === undefined) {
            r.push(b);
        } else if (b === undefined) {
            r.push(a);
        } else {
            r.push(lerp(a, b, t));
        }
    }
    return r;
};
const indexFromRowColumn = (row, column, numRows, numColumns) => row * numColumns + column;
const factorial = (n) => {
    let f = 1;
    for (let i = 1; i <= n; ++i) {
        f *= i;
    }
    return f;
};
const numCombinations = (n, r) => {
    return factorial(n) / (factorial(r) * factorial(n - r));
};
const permutations = (a) => {
    let result = [];
    const permute = (arr, m = []) => {
        if (arr.length === 0) {
            result.push(m)
        } else {
            for (let i = 0; i < arr.length; i++) {
                let curr = arr.slice();
                let next = curr.splice(i, 1);
                permute(curr.slice(), m.concat(next))
            }
        }
    }
    permute(a)
    return result;
};
const combinations = (a, n) => {
    if (n === 0) {
        return [[]];
    }
    const r = [];
    for (let i = 0; i < a.length; ++i) {
        const m = a[i];
        const a_ = a.slice(i + 1);
        const combos = combinations(a_, n - 1);
        combos.forEach(combo => {
            r.push([m].concat(combo));
        });
    }
    return r;
};
const powerSet = (a) => {
    // set of all subsets
    let r = [];
    for (let i = 0; i <= a.length; ++i) {
        const combos = combinations(a, i);
        r = r.concat(combos);
    }
    return r;
};
const clamp = (value, min, max) => {
    if (value < min) { 
        return min;
    }
    if (value > max) {
        return max;
    }
    return value;
};
const browserKeys = [
    ' ', 'Tab', 'Shift', 'Control', 'Alt', 'Meta',
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
    'Escape', 'CapsLock', 'PageUp', 'PageDown', 'Home', 'End'
];
const namespaceFromTag = {
    "svg": SVG_NS,
    "g": SVG_NS,
    "rect": SVG_NS,
    "text": SVG_NS,
    "circle": SVG_NS,
    "line": SVG_NS,
    "use": SVG_NS,
    "image": SVG_NS,
    "path": SVG_NS,
};
const createEl = (attributes) => {
    if (attributes === undefined || attributes === null) { return null; }
    if (attributes instanceof Element) { return attributes; }
    const tag = attributes["tag"] ?? "div";
    const namespace = namespaceFromTag[tag];
    const el = namespace === undefined ? document.createElement(tag) : document.createElementNS(namespace, tag);
    Object.entries(attributes).forEach(([aName, aValue]) => {
        if (aName === "children") {
            for (const child of aValue) {
                if (child) {
                    el.appendChild(
                        child instanceof Element
                        ? child
                        : createEl(child));
                }
            }
        } else if (aName === "class") {
            if (typeof(aValue) === typeof([])) {
                aValue.forEach(v => {
                    if (typeof(v) === "string" && v !== "") {
                        el.classList.add(v);
                    }
                });
            } else {
                if (typeof(aValue) === "string") {
                    el.classList.add(aValue);
                }
            }
        } else if (aName === "text") {
            el.textContent = aValue;
        } else if (aName === "style") {
            Object.entries(aValue).forEach(([aName, aValue]) => {
                el.style[aName] = aValue;
            });
        } else if (aName === "onMount") {
            el.onMount = aValue;
        } else if (aName === "onUnmount") {
            el.onUnmount = aValue;
        } else if (typeof(aValue) === "function") {
            el[aName] = aValue;
        } else {
            el.setAttribute(aName, aValue);
        }
    });
    return el;
};
const moveElToTop = (el) => {
    const parentEl = el.parentElement;
    if (parentEl.lastChild === el) { return; }
    parentEl.removeChild(el);
    parentEl.appendChild(el);
};
const getElementTransformTranslate = (element) => { // this code is from ChatGPT...
    const transform = element.getAttribute("transform");
    if (!transform) return [0, 0]; // no transform yet

    // Match translate(x,y)
    const match = transform.match(/translate\(([^,]+)[ ,]([^,]+)\)/);
    if (match) {
        const x = parseFloat(match[1]);
        const y = parseFloat(match[2]);
        return [x, y];
    }

    return [0, 0];
};
const clientPointToSVG = (clientX, clientY, svg) => {
    const p = new DOMPoint(clientX, clientY);
    const pTransformed = p.matrixTransform(svg.getScreenCTM().inverse());
    return [pTransformed.x, pTransformed.y];
};
function createRect(x, y, width, height) {
    return { x, y, width, height };
}
function boundingRectFromRects(rects) {
    if (rects.length === 0) { return undefined; }
    let minX = rects[0].x;
    let minY = rects[0].y;
    let maxX = minX;
    let maxY = minY;
    for (const rect of rects) {
        minX = Math.min(rect.x, minX);
        maxX = Math.max(rect.x + rect.width, maxX);
        minY = Math.min(rect.y, minY);
        maxY = Math.max(rect.y + rect.height, maxY);
    }
    return createRect(minX, minY, maxX - minX, maxY - minY);
}
function rectsOverlap(a, b) {
    return !(
        a.x > b.x + b.width ||
        b.x > a.x + a.width ||
        a.y > b.y + b.height ||
        b.y > a.y + a.height
    );
}
function rectsOverlapArea(a, b) {
  const overlapX = Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x));
  const overlapY = Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
  return overlapX * overlapY;
}
function pointInRect(x, y, rect) {
    const xOverlap = x >= rect.x && x < rect.x + rect.width;
    const yOverlap = y >= rect.y && y < rect.y + rect.height;
    return xOverlap && yOverlap;
}
function vec2_add(a, b) { 
    return [a[0]+b[0],a[1]+b[1]];
}
function vec2_subtract(a, b) { 
    return [a[0]-b[0],a[1]-b[1]];
}
function vec2_magnitude(a) { 
    return Math.sqrt(a[0]*a[0]+a[1]*a[1]);
}
function vec2_normalize(a) {
    let m = vec2_magnitude(a);
    return [a[0]/m,a[1]/m];
}
function vec2_scale(a, s) {
    return [a[0]*s,a[1]*s];
}
function vec2_dot(a,b) {
    return a[0]*b[0]+a[1]*b[1];
}