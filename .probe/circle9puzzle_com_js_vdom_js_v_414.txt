const VDOM = (function(){

    function create(app, App) {

        { // call onMount or onUnmount when elements are added or removed from the DOM
            function walk(node, callbackName) {
                const callback = node[callbackName];
                if (callback) { callback(node); }
                node.childNodes.forEach(childNode => { walk(childNode, callbackName); });
            }
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    for (const node of mutation.addedNodes) {
                        if (node.nodeType === 1) { // ELEMENT_NODE
                            walk(node, "onMount");
                        }
                    }
                    for (const node of mutation.removedNodes) {
                        if (node.nodeType === 1) { // ELEMENT_NODE
                            walk(node, "onUnmount");
                        }
                    }
                }
            });
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }

        let oldAppVNode;
        refresh = function (changed) {
            // console.time("refresh");
            
            // {
            //     changed = changed ?? [];
            //     if (!Array.isArray(changed)) changed = [changed];
            //     changed = changed.length === 0 ? null : new Set(changed);
            //     changed = (name) => changed === null ? true : changed.has(name);
            // }
            
            {
                const root = document.getElementById("root");
                const newAppVNode = App(app);
                if (!oldAppVNode) {
                    root.appendChild(createEl(newAppVNode));
                } else {
                    refreshElement(root, oldAppVNode, newAppVNode);
                }
                oldAppVNode = newAppVNode;
            }
            
            // console.timeEnd("refresh");
        };
        return { refresh };
    }

    const notAProp = new Set(["tag", "style", "class", "children", "text"]);

    function refreshElement(parent, oldVNode, newVNode, index = 0) {
        const el = parent.childNodes[index];
        if (!el) {  throw new Error(); }

        if (newVNode instanceof Element) {
            if (oldVNode !== newVNode) {
                parent.replaceChild(newVNode, el);
            }
        } else if (!oldVNode && !newVNode) {
            //
        } else if (!oldVNode && newVNode) {
            parent.replaceChild(createEl(newVNode), el);
        } else if (oldVNode && !newVNode) {
            parent.removeChild(el);
        } else if (oldVNode.tag !== newVNode.tag) {
            parent.replaceChild(createEl(newVNode), el);
        } else {
            refreshProperties(el, oldVNode, newVNode);
            refreshClass(el, oldVNode, newVNode);
            refreshStyle(el, oldVNode, newVNode);

            const oldChildren = (oldVNode.children ?? []).filter(it => it != null);
            const newChildren = (newVNode.children ?? []).filter(it => it != null);
            if (oldChildren.length === newChildren.length) {
                const numChildren = newChildren.length;
                let index = 0;
                for (let i = 0; i < numChildren; i += 1) {
                    refreshElement(el, oldChildren[i], newChildren[i], index);
                    if (oldChildren[i]) {
                        index += 1;
                    }
                }
            } else {
                const children = [];
                for (const v of newChildren) {
                    children.push(createEl(v));
                }
                el.replaceChildren(...children);
            }
        }
    }

    function refreshProperties(el, oldVNode, newVNode) {

        function isSpecialPropKey(key, value) {
            return key.startsWith("on") && typeof value === "function";
        }

        function removePropFromEl(el, key) {
            if (isSpecialPropKey(key, el[key])) {
                delete el[key];
            } else {
                el.removeAttribute(key);
            }
        }

        function addPropToEl(el, key, value) {
            if (isSpecialPropKey(key, value)) {
                el[key] = value;
            } else {
                el.setAttribute(key, value);
            }
        }

        const oldProps = oldVNode;
        const newProps = newVNode;

        // update textContent
        if (newProps.text !== undefined) {
            el.textContent = newProps.text;
        }

        // remove old props
        for (let key in oldProps) {
            if (notAProp.has(key)) continue;
            if (!(key in newProps)) {
                removePropFromEl(el, key);
            }
        }

        // set new/changed props
        for (let key in newProps) {
            if (notAProp.has(key)) continue;
            if (oldProps[key] !== newProps[key]) {
                addPropToEl(el, key, newProps[key]);
            }
        }
    }

    function refreshClass(el, oldVNode, newVNode) {
        if (newVNode.class) {
            el.setAttribute("class", newVNode.class.join(" "));
        } else {
            el.removeAttribute("class");
        }
    }

    function refreshStyle(el, oldVNode, newVNode) {
        const oldStyle = oldVNode.style ?? {};
        const newStyle = newVNode.style ?? {};

        // remove old style
        for (let key in oldStyle) {
            if (!(key in newStyle)) {
                el.style.removeProperty(key);
            }
        }

        // set new/changed style
        for (let key in newStyle) {
            if (oldStyle[key] !== newStyle[key]) {
                el.style.setProperty(key, newStyle[key]);
            }
        }
    }

    return { create };
})();

// TODO:jkd move into a different file

function Button({ action }) {
    return {
        tag: "div",
        class: [
            "button", 
            action?.available() ? null : "button-disabled"
        ],
        text: action.text(),
        onclick: (ev) => { 
            if (action.available()) {
                action.execute();
            } 
        },
    };
}

function RadioGroup({ choice, klass }) {
    return {
        tag: "div",
        class: ["tab-group", ...(klass ?? [])],
        style: {
            "padding": "5px",
        },
        children: choice.values.map(value => {
            return {
                tag: "div",
                class: [
                    "tab",
                    choice.currentValue === value && "tab-selected",
                    choice.currentValue !== value && "tab-unselected",
                    choice.available(value) === false && "tab-disabled",
                ],
                text: choice.textToDisplay(value),
                onclick: (ev) => {
                    choice.choose(value);
                }
            }
        })
    };
}

function createChoice(values, onChange, defaultValue, available, textToDisplay) {
    if (values.indexOf(defaultValue) < 0) { defaultValue = undefined; }
    defaultValue = defaultValue ?? values[0];
    available = available ?? function(value) { return true; };
    textToDisplay = textToDisplay ?? function(value) { return value; }
    const r = { values, available, textToDisplay };
    r.currentValue = defaultValue;
    r.choose = (value) => {
        r.currentValue = value;
        if (onChange) onChange(r);
    };
    return r;
};

function createCommandHistory(callbacks, commands_, next_) {
    let commands = commands_ ?? [];
    let next = next_ ?? 0;
    return {
        getCommands: () => commands,
        getNext: () => next,
        doCommand: (command) => {
            if (next !== commands.length) {
                commands = commands.slice(0, next);
            }
            next += 1;
            commands.push(command);
            if (callbacks?.do) {
                if (command[0] === "group") {
                    const subcommands = command[1];
                    for (const subcommand of subcommands) {
                        callbacks.do(subcommand);
                    }
                } else {
                    callbacks.do(command);
                }
            }
        },
        actions: {
            undo: {
                text: () => "Undo",
                available: () => next > 0,
                execute: () => {
                    next -= 1;
                    if (callbacks?.undo) {
                        const command = commands[next];
                        if (command[0] === "group") {
                            const subcommands = command[1];
                            for (const subcommand of reverseArray(subcommands)) {
                                callbacks.undo(subcommand);
                            }
                        } else {
                            callbacks.undo(command);
                        }
                    }
                    V.refresh("history");
                }
            },
            redo: {
                text: () => "Redo",
                available: () => next < commands.length,
                execute: () => {
                    next += 1;
                    if (callbacks?.redo) {
                        const command = commands[next - 1];
                        if (command[0] === "group") {
                            const subcommands = command[1];
                            for (const subcommand of subcommands) {
                                callbacks.redo(subcommand);
                            }
                        } else {
                            callbacks.redo(command);
                        }
                    }
                    V.refresh("history");
                }
            },
            restart: {
                text: () => "Reset",
                available: () => commands.length > 0,
                execute: () => {
                    if (confirm("Reset the puzzle?")) {
                        commands = [];
                        next = 0;
                        V.refresh("history");
                        if (callbacks?.restart) callbacks.restart();
                    }
                }
            },
        },
    };
}

function CommandHistoryControls({ commandHistory }) {
    return [
        Button({ action: commandHistory.actions.restart }),
        Button({ action: commandHistory.actions.undo }),
        Button({ action: commandHistory.actions.redo }),
    ];
    // return {
    //     tag: "div",
    //     class: ["button-row"],
    //     style: {
    //         padding: "10px"
    //     },
    //     children: [
    //         Button({ action: commandHistory.actions.restart }),
    //         Button({ action: commandHistory.actions.undo }),
    //         Button({ action: commandHistory.actions.redo }),
    //     ],
    // };
}