const initPage = (width, height) => {
    refreshTheme();
    width = width || 480; // XXX:jkd remove
    height = height || width; // XXX:jkd remove
    // handlePortraitOrLandscape(width, height); // XXX:jkd remove
    versionCheckAndFix();
    // { // https://discourse.threejs.org/t/iphone-how-to-remove-text-selection-magnifier/47812/12
    //     function createDoubleTapPreventer(timeout_ms) {
    //         let dblTapTimer = 0;
    //         let dblTapPressed = false;
        
    //         return function (e) {
    //             clearTimeout(dblTapTimer);
    //             if (dblTapPressed) {
    //                 e.preventDefault();
    //                 dblTapPressed = false;
    //             } else {
    //                 dblTapPressed = true;
    //                 dblTapTimer = setTimeout(() => {
    //                     dblTapPressed = false;
    //                 }, timeout_ms);
    //             }
    //         };
    //     }
    //     document.body.addEventListener("touchstart", createDoubleTapPreventer(500), { passive: false });
    // }
};
const [handlePurchaseUrl, checkForPlus, getPlusDaysRemaining, getPlusYear, versionCheckAndFix] = (() => {
    const products = {
        "a4090491df2741d4d4f51671037e37126ac58fddeea85623977bafef84adab0e": {name: "PLUS 2024", kind: "plus", year: 2024},
        "fbcb4d516b17ed852538ff53f97289b01fed38ff09ace868b7d9c67be46db588": {name: "PLUS 2025", kind: "plus", year: 2025},
        "e350266e44561673c0ad05583878498f295954191b8dbb549a7e8596272f2082": {name: "PLUS 2026", kind: "plus", year: 2026},
    };
    const getPurchasedTable = () => {
        let purchasedTable = {};
        {
            const s = window.localStorage.getItem("site|purchased");
            if (s !== null) {
                purchasedTable = JSON.parse(s);
            }
        }
        return purchasedTable;
    };
    const getLatestPlusYearPurchased = () => {
        const checkPurchased = (uuidHash) => {
            const purchasedTable = getPurchasedTable();
            let purchased = false;
            Object.keys(purchasedTable).forEach(purchasedUuid => {
                const purchasedUuidHash = SHA256.hash(purchasedUuid);
                if (purchasedUuidHash === uuidHash) {
                    purchased = true;
                }
            });
            return purchased;
        };
        let latest = undefined;
        Object.entries(products).forEach(([uuidHash, product]) => {
            if (product.kind === "plus") {
                if (checkPurchased(uuidHash)) {
                    if (latest === undefined || latest < product.year) {
                        latest = product.year;
                    }
                }
            }
        });
        return latest;
    };
    const activatePurchase = (uuid) => {
        const purchasedTable = getPurchasedTable();
        if (purchasedTable[uuid] !== undefined) { return false; }
        purchasedTable[uuid] = "";
        window.localStorage.setItem("site|purchased", JSON.stringify(purchasedTable));
        return true;
    };
    const datePlusNMonths = (date, N) => {
        return new Date(new Date(date).setMonth(date.getMonth() + N));
    };
    const datePlusNDays = (date, N) => {
        return new Date(new Date(date).setDate(date.getDate() + N));
    };
    const numDaysBetweenDates = (fromDate, toDate) => {
        const oneDay = 24 * 60 * 60 * 1000; // hours * minutes * seconds * milliseconds
        const diffDays = Math.round((toDate.getTime() - fromDate.getTime()) / oneDay);
        return diffDays;
    };
    const getPlusYear = () => getLatestPlusYearPurchased();
    const getPlusDaysRemaining = (now) => {
        const plusYear = getLatestPlusYearPurchased();
        if (plusYear === undefined) { return undefined; }
        const expiryDate = new Date(plusYear + 1, 0, 1);
        const numDaysRemaining = numDaysBetweenDates(now, expiryDate);
        return numDaysRemaining;
    };
    const checkForPlus = (now) => getPlusDaysRemaining(now) >= -7;
    const handlePurchaseUrl = (now) => {
        const url = new URL(window.location.toLocaleString());
        const uuid = url.searchParams.get("purchased");
        if (uuid === null) { return; }
        const digest = SHA256.hash(uuid);
        const product = products[digest];
        if (product === undefined) { 
            setTimeout(() => {
                alert("Invalid product ID."); 
            }, 100);
            return; 
        }
        if (now.getFullYear() > product.year) {
            history.replaceState(null, "", ".");
            setTimeout(() => {
                alert(`${product.name} has expired.`); 
            }, 100);
            return; 
        }
        const activated = activatePurchase(uuid);
        if (activated) {
            history.replaceState(null, "", ".");
            setTimeout(() => {
                alert(`Thank you for purchasing ${product.name}. Enjoy!`);
                window.location.reload();
            }, 100);
            return;
        } else {
            history.replaceState(null, "", ".");
            setTimeout(() => {
                alert(`${product.name} has already been activated.`); 
            }, 100);
            return;
        }
    };
    const versionCheckAndFix = () => {
        const versionKey = "site|version";
        const latestVersion = 5;
        const currentVersionS = window.localStorage.getItem("site|version");
        const currentVersion = typeof(currentVersionS) === "string" ? Number(currentVersionS) : undefined; 
        if (currentVersion !== undefined && currentVersion >= latestVersion) { 
            // good
            return; 
        }
        { // fix
            // Object.keys(window.localStorage).forEach(key => {
            //     if (key.startsWith("site|")) {
            //     } else if (key.includes("|setting|")) {
            //     } else {
            //         window.localStorage.removeItem(key);
            //     }
            // });
            window.localStorage.setItem(versionKey, latestVersion);
        }
    };
    return [handlePurchaseUrl, checkForPlus, getPlusDaysRemaining, getPlusYear, versionCheckAndFix];
})();
const createTabGroup = (values, initialValue, onChange) => {
    const tabGroup = {values, value: undefined};
    tabGroup.groupE = document.createElement("div");
    tabGroup.groupE.classList.add("tab-group");
    tabGroup.tabs = {};
    tabGroup.values = values;
    values.forEach(value => {
        const tab = document.createElement("span");
        tabGroup.groupE.appendChild(tab);
        tabGroup.tabs[value] = tab;
        tab.textContent = `${value}`;
        tab.classList.add("tab");
        tab.onpointerdown = function(ev) {
            setTabGroupValue(tabGroup, value);
        };
    });
    setTabGroupValue(tabGroup, initialValue);
    tabGroup.onChange = onChange;
    return tabGroup;
};
const setTabGroupValue = (tabGroup, value) => {
    if (tabGroup.tabs[value] === undefined) {
        value = tabGroup.values[0];
    }
    tabGroup.value = value;
    tabGroup.values.forEach(v => {
        const tab = tabGroup.tabs[v];
        if (v == value) {
            tab.classList.add("tab-selected");
            tab.classList.remove("tab-unselected");
        } else {
            tab.classList.add("tab-unselected");
            tab.classList.remove("tab-selected");
        }
    });
    if (tabGroup.onChange) {
        tabGroup.onChange(tabGroup);
    }
};
const siteSettings = [
    { id: "theme", text: "Theme", kind: "choice", values: ["Auto", "Light", "Dark"], defaultValue: "Auto", },
    { id: "clock", text: "Clock", kind: "choice", values: ["Show", "Hide"], defaultValue: "Show", },
];
const findSiteSetting = (id) => {
    let r;
    siteSettings.forEach(setting => {
        if (setting.id === id) {
            r = setting;
        }
    });
    return r;
};
const settingLocalStorageKey = (settingId, genreId) => {
    const isSettingSiteWide = (settingId) => {
        let r = false;
        siteSettings.forEach(setting => {
            if (setting.id === settingId) { r = true; }
        });
        return r;
    };
    if (isSettingSiteWide(settingId)) {
        return `site|setting|${settingId}`;
    } else if (genreId !== undefined) {
        return `${genreId}|setting|${settingId}`;
    } else {
        return undefined;
    }
};
const loadSetting = (setting, genreId) => {
    const lskey = settingLocalStorageKey(setting.id, genreId);
    const s = window.localStorage.getItem(lskey);
    if (s === null) {
        return setting.defaultValue;
    } else {
        const value = JSON.parse(s);
        return value;
    }
};
const rgbFromCssColorTable = {};
const rgbFromCssColorUsing1x1Canvas = (cssColor) => {
    const canvas = document.createElement("canvas");
    canvas.width = 1;
    canvas.height = 1;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = cssColor;
    ctx.fillRect(0, 0, 1, 1);
    const pixel = ctx.getImageData(0, 0, 1, 1).data;
    const r = pixel[0];
    const g = pixel[1];
    const b = pixel[2];
    const a = pixel[3] !== undefined ? pixel[3] : 1;
    return [r, g, b, a];
};
const cssComputedStyleColor = (cssColor) => {
    const e = document.createElement("div");
    e.style.color = cssColor;
    document.body.appendChild(e);
    const computedColorString = window.getComputedStyle(e).color;
    document.body.removeChild(e);
    return computedColorString;
};
const rgbFromCssColor = (cssColor) => {
    if (rgbFromCssColorTable[cssColor] !== undefined) {
        return rgbFromCssColorTable[cssColor];
    }
    const computed = cssComputedStyleColor(cssColor);
    const rgb = rgbFromCssColorUsing1x1Canvas(computed);
    rgbFromCssColorTable[cssColor] = rgb;
    return rgb;
};
const cssFromRgb = (rgb) => `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${rgb[3]})`;
const cssColorMix = (fromCssColor, toCssColor, t) => {
    const fromRgb = rgbFromCssColor(fromCssColor);
    const toRgb = rgbFromCssColor(toCssColor);
    const rgb = lerpArray(fromRgb, toRgb, t);
    const css = cssFromRgb(rgb);
    return css;
};
const darkThemeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
const refreshTheme = () => {
    {
        Object.keys(rgbFromCssColorTable).forEach(k => {
            delete rgbFromCssColorTable[k];
        });
    }
    const root = document.querySelector(":root");
    root.classList.remove("theme-light");
    root.classList.remove("theme-dark");
    const s =localStorage.getItem("setting|site|theme");
    const themeSettingValue = typeof s == "string" ? JSON.parse(s) : "Auto";
    const inAuto = themeSettingValue === "Auto";
    const isSystemInDarkMode = darkThemeMediaQuery.matches;
    if (themeSettingValue === "Light" || (inAuto && !isSystemInDarkMode)) { root.classList.add("theme-light"); }
    if (themeSettingValue === "Dark"  || (inAuto && isSystemInDarkMode)) { root.classList.add("theme-dark"); }
};
{
    darkThemeMediaQuery.onchange = () => { refreshTheme(); };
    refreshTheme();
}
PUZZLEUTIL.page = {};
// PUZZLEUTIL.page.createPuzzlePage = (logoUrl, gameTitle, helpE, date, genreId, genre, categories, puzzlesByCategory, isPlusOnly) => {
//     // {
//     //     const newCategories = [];
//     //     const newPuzzlesByCategory = {};
//     //     // const table = ["1","2","3","4","5"]; 
//     //     // const table = ["I","II","III","IV","V"]; 
//     //     const table = ["A","B","C","D","E"]; 
//     //     for (let i = 0; i < categories.length; ++i) {
//     //         const s = table[i];
//     //         newCategories.push(s);
//     //         newPuzzlesByCategory[s] = puzzlesByCategory[categories[i]];
//     //     }
//     //     categories = newCategories;
//     //     puzzlesByCategory = newPuzzlesByCategory;
//     // }
//     // {
//     //     const ensureAllPuzzlesHaveSolutions = () => {
//     //         categories.forEach(category => {
//     //             const puzzles = puzzlesByCategory[category];
//     //             puzzles.forEach((desc, index) => {
//     //                 const model = genre.createModel(desc);
//     //                 const name = `${genreId}-${category}-${index+1}-${puzzles.length}`;
//     //                 const hasSolution = model.solutionState !== undefined;
//     //                 console.log(`${hasSolution?"[ OK ]":"[FAIL]"} ${name}`);
//     //                 if (!hasSolution) {
//     //                     const s = genre.solve.solve(desc);
//     //                     const content = `'${desc}': '${s}',\n`;
//     //                     downloadContent(content, `${name}.solution`);
//     //                 }
//     //             });
//     //         });
//     //     };
//     //     ensureAllPuzzlesHaveSolutions();
//     // }
//     const puzzlePageE = document.getElementById("puzzle-page");
//     const pageTop = createEl({ tag: "div", class: ["puzzle-page-top"] });
//     const pageMiddle = createEl({ tag: "div", class: ["puzzle-page-middle"] });
//     const pageBottom = createEl({ tag: "div", class: ["puzzle-page-bottom"] });

//     let thePuzzleArea;
//     const settingsValues = {};
//     const allSettings = genre.settings ? siteSettings.concat(genre.settings) : siteSettings;
//     allSettings.forEach(setting => {
//         settingsValues[setting.id] = loadSetting(setting, genreId);
//     });
//     refreshTheme();
//     const topE = pageTop;
//     const topLeftE = createEl({ tag: "div", class: ["logo-title-and-date"] }); 
//     const topRightE = createEl({ tag: "div", class: ["button-row", "button-row-help-settings-menu"] });
//     const makeButton = (text) => {
//         const e = document.createElement("div");
//         e.classList.add("button");
//         e.classList.add("button-small");
//         e.textContent = text;
//         return e;
//     };
//     const fullscreenButton = makeButton("");
//     const refreshFullscreenButtonText = (isFullscreen) => {
//         fullscreenButton.textContent = isFullscreen ? "Min." : "Max.";
//     };
//     refreshFullscreenButtonText(false);
//     fullscreenButton.onclick = (ev) => {
//         const el = document.querySelector(".puzzle-page");
//         if (el.requestFullscreen) {
//             if (!document.fullscreenElement) {
//                 el.requestFullscreen();
//                 refreshFullscreenButtonText(true);
//             } else {
//                 document.exitFullscreen();
//                 refreshFullscreenButtonText(false);
//             }
//         } else {
//             const klass = "fake-fullscreen";
//             addOrRemoveClass(el, klass, !el.classList.contains(klass));
//         }
//     };
//     const helpButton = makeButton("Help");
//     const settingsButton = makeButton("Settings");
//     const menuButton = makeButton("Menu");
//     topRightE.appendChild(helpButton);
//     // if (document.body.requestFullscreen) {
//     //     // TODO:jkd
//     //     // only show fullscreen button if it is supported.
//     //     // unfortunately, it is not supported on ios safari
//     //     topRightE.appendChild(fullscreenButton);
//     // }
//     topRightE.appendChild(settingsButton);
//     topRightE.appendChild(menuButton);
//     const logoSize = 30;
//     const logoImg = Object.assign(document.createElement("img"), {
//          src: logoUrl,
//          width: logoSize,
//          height: logoSize
//     });
//     const logoTextE = document.createElement("div");
//     logoTextE.style.fontSize = "24px";
//     logoTextE.style.fontFamily = "TitleFont";
//     logoTextE.textContent = gameTitle;
//     const logoE = document.createElement("div");
//     logoE.classList.add("no-browser-stuff");
//     logoE.classList.add("icon-top");
//     // logoE.classList.add("button");
//     logoE.appendChild(logoImg);
//     logoE.appendChild(logoTextE);
//     const makeDialog = (title) => {
//         const dialogE = document.createElement("div");
//         const padding = "10px";
//         Object.assign(dialogE.style, {
//             width: "100%",
//             "box-sizing": "border-box",
//             color: "var(--theme-text)",
//             backgroundColor: "var(--theme-glass)",
//             padding: `${padding}`,
//             marginBottom: "15px",
//             display: "none",
//         });
//         const topDiv = document.createElement("div");
//         Object.assign(topDiv.style, {
//             display: "flex",
//             flexDirection: "row",
//             justifyContent: "space-between",
//             marginBottom: "5px",
//             padding: "5px",
//         });
//         topDiv.classList.add("heading");
//         const titleE = document.createElement("div");
//         titleE.textContent = title;
//         Object.assign(titleE.style, {
//             width: "85%",
//             fontSize: "1.25rem",
//             display: "flex",
//             "align-items": "center"
//         });
//         const closeButton = makeButton("x");
//         closeButton.onclick = () => {
//             dialogE.style.display = "none";
//         };
//         topDiv.appendChild(titleE);
//         topDiv.appendChild(closeButton);
//         dialogE.appendChild(topDiv);
//         return dialogE;
//     };
//     const makeHelpDialog = () => {
//         const dialog = makeDialog("Help");
//         dialog.appendChild(helpE);
//         helpE.style["text-align"] = "justify";
//         helpE.style.display = "";

//         const solutionDiv = document.createElement("div");
//         solutionDiv.style = "padding-top: 10px;";
//         let showSolutionButton;
//         let isSolutionShown = false;

//         const showSolution = (show) => {
//             solutionDiv.innerHTML = "";
//             if (show) {
//                 const view = thePuzzleArea.theCurrentPuzzle.view;
//                 const desc = view.desc;
//                 const model = view.model;
//                 const view2 = genre.createView(model, model.solutionState, /*scale=*/0.60, /*isSolution=*/true);
//                 view2.model = model;
//                 view2.state = model.solutionState;
//                 view2.root.style["pointer-events"] = "none";
//                 view2.root.classList.remove("expandable-svg");
//                 view2.root.querySelectorAll("expandable-svg").forEach(el => {
//                     el.classList.remove("expandable-svg");
//                 });
//                 const dummyHooks = {
//                     doCommandAndWriteToHistory: () => {},
//                     getPuzzleSetInfo: () => {},
//                     clearModality: () => {},
//                     setModalityTo: () => {},
//                     markHintUsed: () => {},
//                     getModality: () => {},
//                 };
//                 view2.hooks = dummyHooks;
//                 genre.refreshView(view2);
//                 solutionDiv.appendChild(view2.root);
//             }
//             solutionDiv.style["display"] = show ? "" :"none";
//             showSolutionButton.textContent = show ? "Hide Solution" : "Reveal Solution"; 
//         };

//         const solutionAreaDiv = document.createElement("div");
//         dialog.appendChild(solutionAreaDiv);

//         {
//             const e = document.createElement("div");
//             solutionAreaDiv.appendChild(e);
//             e.innerHTML = "<br><b>Solution</b>";
//         }

//         solutionAreaDiv.appendChild(solutionDiv);

//         {
//             const buttonRow = document.createElement("div");
//             solutionAreaDiv.appendChild(buttonRow);
//             buttonRow.classList.add("button-row");
//             buttonRow.style["margin-top"] = "10px";
//             showSolutionButton = makeButton("Reveal"); buttonRow.appendChild(showSolutionButton);
//             showSolutionButton.onclick = () => {
//                 isSolutionShown = !isSolutionShown; 
//                 showSolution(isSolutionShown);
//                 thePuzzleArea.markHintUsed();
//             };
//             if (genre.hint !== undefined) {
//                 const hintButton = makeButton("Hint"); 
//                 buttonRow.appendChild(hintButton);
//                 hintButton.onclick = () => {
//                     thePuzzleArea.doHint();
//                 };
//             }
//             if (!genre.disableConfirm) {
//                 const confirmButton = makeButton("Correct?"); buttonRow.appendChild(confirmButton);
//                 confirmButton.onclick = () => {
//                     thePuzzleArea.doConfirm();
//                 };
//             }
//         }


//         const showSolutionArea = (show) => {
//             solutionAreaDiv.style["display"] = show ? "" : "none";
//         };

//         return [dialog, showSolution, showSolutionArea];
//     };
//     const onChangeSetting = (settingId) => {
//         const newValue = settingsValues[settingId];
//         const lskey = settingLocalStorageKey(settingId, genreId);
//         const s = JSON.stringify(newValue);
//         window.localStorage.setItem(lskey, s);
//         refreshTheme();
//         thePuzzleArea.refresh();
//     };
//     const makeSettingsDialog = () => {
//         const dialog = makeDialog("Settings");
//         const makeSettingRow = (label) => {
//             const rowE = document.createElement("div");
//             rowE.classList.add("setting-row");
//             const labelE = document.createElement("div");
//             labelE.textContent = label;
//             labelE.classList.add("setting-label");
//             rowE.appendChild(labelE);
//             return rowE;
//         };
//         const makeCheckbox = (setting) => {
//             const e = document.createElement("div");
//             Object.assign(e.style, {
//                 display: "flex",
//                 flexDirection: "row",
//                 justifyContent: "left",
//             });
//             const checkbox = document.createElement("input");
//             checkbox.type = "checkbox";
//             checkbox.id = setting.id;
//             checkbox.checked = settingsValues[setting.id];
//             checkbox.onchange = (ev) => {
//                 const newValue = checkbox.checked;
//                 settingsValues[setting.id] = newValue;
//                 onChangeSetting(setting.id);
//             };
//             e.appendChild(checkbox);
//             return e;
//         };
//         const makeChoice = (setting) => {
//             const onChange = (tabGroup) => {
//                 const newValue = tabGroup.value;
//                 settingsValues[setting.id] = newValue;
//                 onChangeSetting(setting.id);
//             };
//             const tabGroup = createTabGroup(setting.values, settingsValues[setting.id], onChange);
//             return tabGroup.groupE;
//         };
//         const makeElement = (setting) => {
//             if (setting.kind === "boolean") { return makeCheckbox(setting); }
//             if (setting.kind === "choice") { return makeChoice(setting); }
//         };
//         {
//             const hr = document.createElement("hr");
//             dialog.appendChild(hr);
//         }
//         allSettings.forEach(setting => {
//             const rowE = makeSettingRow(setting.text);
//             const e = makeElement(setting);
//             if (e !== undefined) {
//                 rowE.appendChild(e);
//             }
//             dialog.appendChild(rowE);
//             const hr = document.createElement("hr");
//             dialog.appendChild(hr);
//         });
//         return dialog;
//     };
//     const [helpDialog, showSolution, showSolutionArea] = makeHelpDialog();
//     const settingsDialog = makeSettingsDialog();
//     const allDialogs = [helpDialog, settingsDialog];
//     const dateE = document.createElement("div");
//     dateE.classList.add("no-browser-stuff");
//     dateE.textContent = date.toLocaleDateString("default", {dateStyle: "long"}); 
//     topLeftE.appendChild(logoE);
//     topE.appendChild(topLeftE);
//     const onPuzzleChange = (puzzleView) => {
//         showSolution(false);
//         showSolutionArea(puzzleView.model.solutionState !== undefined);
//     };
//     const hideAllDialogs = () => {
//         allDialogs.forEach(dialog => {
//             dialog.style.display = "none";
//         });
//     };
//     const showDialog = (dialog) => {
//         hideAllDialogs();
//         dialog.style.display = "";
//     };
//     puzzlePageE.appendChild(pageTop);
//     puzzlePageE.appendChild(pageMiddle);
//     puzzlePageE.appendChild(pageBottom);

//     const puzzleArea = PUZZLEUTIL.page.createPuzzleArea(
//         date, 
//         genreId, 
//         genre, 
//         isPlusOnly,
//         categories, 
//         puzzlesByCategory,
//         settingsValues,
//         onPuzzleChange,
//         hideAllDialogs
//     );
//     pageMiddle.insertBefore(helpDialog, pageMiddle.firstChild);
//     pageMiddle.insertBefore(settingsDialog, pageMiddle.firstChild);
//     topE.appendChild(topRightE);
//     thePuzzleArea = puzzleArea;
//     {
//         const e = document.createElement("div");
//         e.id = "solved-animation";
//         e.classList.add("solved-animation");
//         document.querySelector(".puzzle-page").appendChild(e);
//     }
//     // pageMiddle.appendChild(puzzleArea.rootE);
//     { // interactivity
//         // logoE.onclick = () => {
//         //     window.location = "..";
//         // };
//         menuButton.onclick = () => {
//             window.location = "..";
//         };
//         helpButton.onclick = () => {
//             showDialog(helpDialog);
//         };
//         settingsButton.onclick = () => {
//             showDialog(settingsDialog);
//         };
//     }
//     const puzzlePage = {
//         theCurrentPuzzle: thePuzzleArea.theCurrentPuzzle
//     };
//     thePuzzlePage = puzzlePage;
//     return puzzlePage;
// };
// PUZZLEUTIL.page.createPuzzleArea = (
//         date, 
//         genreId, 
//         genre, 
//         isPlusOnly, 
//         categories, 
//         puzzlesByCategory, 
//         settingsValues, 
//         onPuzzleChange,
//         hideAllDialogs) => 
// {
//     const hashAndSelectPuzzle = (dateString, category, dailyPlus, setNumber) => {
//         const puzzleList = puzzlesByCategory[category];
//         const dateString_ = dailyPlus === "Sample" ? "" : dateString;
//         const s = `${dateString_} ${category} ${dailyPlus} ${setNumber}`;
//         const h = cyrb53(s);
//         const i = h % puzzleList.length;
//         const p = puzzleList[i];
//         return p;
//     };
//     const getSamplePuzzles = () => {
//         if (!isPlusOnly) { return []; }
//         const puzzleIds = [];
//         categories.forEach(category => {
//             const p = hashAndSelectPuzzle(undefined, category, "Sample", 0);
//             const puzzleId = genre.getPuzzleId(p);
//             puzzleIds.push(puzzleId);
//         });
//         return puzzleIds;
//     };
//     const dateString = `${date.getDate()} ${date.getMonth()+1} ${date.getFullYear()}`;
//     const plus = "Plus";
//     { // start a new day?
//         const dateKey = `${genreId}|date`;
//         if (window.localStorage.getItem(dateKey) != dateString) {
//             // start a new day!
//             const samplePuzzleIds = getSamplePuzzles();
//             const isSamplePuzzleKey = (key) => {
//                 for (let i = 0; i < samplePuzzleIds.length; ++i) {
//                     const id = samplePuzzleIds[i];
//                     if (key.includes(`|${id}`)) {
//                         return true;
//                     }
//                 }
//                 return false;
//             };
//             const allKeys = Object.keys(window.localStorage);
//             allKeys.forEach((key) => {
//                 if (key.startsWith(`${genreId}|`)) {
//                     if (key.startsWith(`${genreId}|setting|`)) {
//                     } else if (isSamplePuzzleKey(key)) {
//                     } else {
//                         window.localStorage.removeItem(key);
//                     }
//                 }
//             });
//             window.localStorage.setItem(dateKey, dateString);
//         }
//     }
//     let plusCount = 0;
//     {
//         const v = window.localStorage.getItem(`${genreId}|plusCount`);
//         if (v != null) {
//             const n = Number(v);
//             if (n != undefined && !isNaN(n)) {
//                 plusCount = n;
//             }
//         }
//     }
//     let theCurrentPuzzle = {
//         view: undefined,
//         isSolved: false,
//         hintUsed: false,
//         clockTime: undefined,
//     };
//     const savePuzzleState = (view) => {
//         const stateKey = getPuzzleStateLocalStorageKey(view.desc);
//         const stateString = genre.stringifyState(view.model, view.state);
//         window.localStorage.setItem(stateKey, stateString);
//         const historyKey = getPuzzleHistoryLocalStorageKey(view.desc);
//         const historyString = JSON.stringify(view.history);
//         window.localStorage.setItem(historyKey, historyString);
//     };

//     const getCurrentPuzzleId = () => {
//         const view = theCurrentPuzzle.view;
//         if (view === undefined) { return undefined; }
//         const puzzleId = genre.getPuzzleId(view.desc);
//         return puzzleId;
//     };

//     const saveDataWithPuzzle = (puzzleId, key, data) => {
//         const fullKey = `${genreId}|${key}|${puzzleId}`;
//         const s = JSON.stringify(data);
//         window.localStorage.setItem(fullKey, s);
//     };
//     const loadDataWithPuzzle = (puzzleId, key, defaultData) => {
//         const fullKey = `${genreId}|${key}|${puzzleId}`;
//         const s = window.localStorage.getItem(fullKey);
//         if (s === null) { return defaultData; }
//         const data = JSON.parse(s);
//         return data;
//     };
//     const pageTop = document.querySelector(".puzzle-page-top");
//     const pageMiddle = document.querySelector(".puzzle-page-middle");
//     const pageBottom = document.querySelector(".puzzle-page-bottom");
//     const isPlusEnabled = checkForPlus(date);
//     const dailyPlus = isPlusOnly 
//         ? (isPlusEnabled ? [plus] : ["Sample",plus]) 
//         : ["Daily", plus];
//     let dailyPlusInitialValue = window.localStorage.getItem(`${genreId}|dailyPlusTab`);
//     let categoryInitialValue = window.localStorage.getItem(`${genreId}|categoryTab`);
//     if (!isPlusEnabled) {
//         dailyPlusInitialValue = null;
//     }
//     dailyPlusInitialValue = dailyPlusInitialValue || dailyPlus[0];
//     categoryInitialValue = categoryInitialValue || categories[0];
//     const categoryTabGroup = createTabGroup(categories, categoryInitialValue, (tabGroup) => {
//         goToPuzzle(); 
//     });
//     const dailyPlusTabGroup = createTabGroup(dailyPlus, dailyPlusInitialValue, (tabGroup) => {
//         if (!isPlusEnabled && tabGroup.value == plus) {
//             setTabGroupValue(tabGroup, "Daily");
//             return;
//         }
//         goToPuzzle();
//     });
//     if (!isPlusEnabled) {
//         const tab = dailyPlusTabGroup.tabs[plus];
//         if (tab !== undefined) {
//             tab.classList.add("tab-disabled");
//         }
//     }
//     const refreshCategoryTabGroupCheckmarks = () => {
//         const dailyPlus = dailyPlusTabGroup.value;
//         categories.forEach(category => {
//             const isPlus = (dailyPlus === plus);
//             const setNumber = isPlus ? plusCount : 0;
//             const desc = hashAndSelectPuzzle(dateString, category, dailyPlus, setNumber);
//             const puzzleId = genre.getPuzzleId(desc);
//             const isSolved = loadDataWithPuzzle(puzzleId, "solved", false);
//             const checkmark = isSolved ? " ✓" : "";
//             categoryTabGroup.tabs[category].textContent = `${category}${checkmark}`;
//         });
//     };
//     refreshCategoryTabGroupCheckmarks();
//     const buttons = {};
//     let timerE;
//     { // tab groups
//         const tabGroupsE = document.createElement("div");
//         tabGroupsE.classList.add("tab-groups");
//         tabGroupsE.classList.add("daily-plus-category-tab-groups");
//         tabGroupsE.appendChild(dailyPlusTabGroup.groupE);
//         tabGroupsE.appendChild(categoryTabGroup.groupE);
//         // tabGroupsE.style.display = "none";
//         pageTop.querySelector(".logo-title-and-date").appendChild(tabGroupsE);
//     }
//     let modality = undefined;
//     const clearModality = () => {
//         modality = undefined;
//         if (theCurrentPuzzle.view !== undefined) {
//             theCurrentPuzzle.view.check = undefined;
//             theCurrentPuzzle.view.hint = undefined;
//         }
//         statusLine.hide();
//     }
//     const getModality = () => {
//         return modality;
//     };
//     const setModalityTo = (modality_, text) => {
//         clearModality();
//         modality = modality_;
//         statusLine.showText(text);
//     } ;
//     const setModalityToHint = (hint) => {
//         clearModality();
//         modality = "hint";
//         theCurrentPuzzle.view.hint = hint;
//     };
//     const setModalityToCheck = (check) => {
//         clearModality();
//         modality = "check";
//         theCurrentPuzzle.view.check = check;
//     };
//     const statusLine = PUZZLEUTIL.page.createStatusLine();
//     const puzzlePageE = document.getElementById("puzzle-page");
//     const bottom = puzzlePageE.querySelector(".puzzle-page-bottom");
//     { // buttons
//         const buttonsLRE = document.createElement("div");
//         bottom.appendChild(buttonsLRE);
//         buttonsLRE.classList.add("button-row-lr");
//         const buttonsLE = document.createElement("div");
//         buttonsLRE.appendChild(buttonsLE);
//         buttonsLE.classList.add("button-row");
//         { // status line
//             buttonsLRE.appendChild(statusLine.e);
//         }
//         { // timer element
//             timerE = document.createElement("div");
//             timerE.classList.add("clock");
//             buttonsLRE.appendChild(timerE);
//             timerE.textContent = "";
//         }
//         const buttonsRE = document.createElement("div");
//         buttonsLRE.appendChild(buttonsRE);
//         buttonsRE.classList.add("button-row");
//         { // new button
//             const buttonE = document.createElement("span");
//             dailyPlusTabGroup.groupE.appendChild(buttonE);
//             buttonE.classList.add("button");
//             buttonE.classList.add("button-small");
//             buttonE.classList.add("button-plus");
//             buttonE.textContent = "+";
//             buttons["new"] = buttonE;
//         }
//         { // restart button
//             const buttonE = document.createElement("span");
//             buttonsLE.appendChild(buttonE);
//             buttonE.classList.add("button");
//             buttonE.textContent = "Reset";
//             buttons["restart"] = buttonE;
//             if (genre.hideRestartButton) {
//                 buttonE.style.display = "none";
//             }
//         }
//         { // undo button
//             const buttonE = document.createElement("span");
//             buttonsLE.appendChild(buttonE);
//             buttonE.classList.add("button");
//             // buttonE.classList.add("button-small");
//             // buttonE.textContent = "<";
//             buttonE.textContent = "< Undo";
//             buttons["undo"] = buttonE;
//             if (genre.hideUndoRedoButtons) {
//                 buttonE.style.display = "none";
//             }
//         }
//         { // redo button
//             const buttonE = document.createElement("span");
//             buttonsLE.appendChild(buttonE);
//             buttonE.classList.add("button");
//             // buttonE.classList.add("button-small");
//             // buttonE.textContent = ">";
//             buttonE.textContent = "Redo >";
//             buttons["redo"] = buttonE;
//             if (genre.hideUndoRedoButtons) {
//                 buttonE.style.display = "none";
//             }
//         }

//         { // check button
//             const buttonE = document.createElement("span");
//             buttonsRE.appendChild(buttonE);
//             buttonE.classList.add("button");
//             buttonE.textContent = "Check";
//             buttons["check"] = buttonE;
//             if (genre.hideCheckButton) {
//                 buttonE.style.display = "none";
//             }
//         }
//     }
//     const getPuzzleSetInfo = () => {
//         const dailyPlus = dailyPlusTabGroup.value;
//         const isPlus = (dailyPlus === plus);
//         const info = [];
//         categories.forEach(category => {
//             const setNumber = isPlus ? plusCount : 0;
//             const desc = hashAndSelectPuzzle(dateString, category, dailyPlus, setNumber);
//             const puzzleId = genre.getPuzzleId(desc);
//             const isSolved = loadDataWithPuzzle(puzzleId, "solved", false);
//             const hintUsed = loadDataWithPuzzle(puzzleId, "hintUsed", false);
//             const clockTime = loadDataWithPuzzle(puzzleId, "clockTime", 0);
//             info.push({category, setNumber, desc, puzzleId, isSolved, hintUsed, clockTime});
//         });
//         return info;
//     };
//     const scrollPuzzleIntoView = () => {
//         const view = theCurrentPuzzle.view;
//         if (view === undefined) { return; }
//         view.root.scrollIntoView({behavior: "smooth"});
//     };
//     const canUndo = (history) => history.undoCount < history.commands.length; 
//     const canRedo = (history) => history.undoCount > 0; 
//     const refreshUndoRedoButtons = () => {
//         const view = theCurrentPuzzle.view;
//         addOrRemoveClass(buttons["undo"], "button-disabled", !canUndo(view.history));
//         addOrRemoveClass(buttons["redo"], "button-disabled", !canRedo(view.history));
//         addOrRemoveClass(buttons["restart"], "button-disabled", !canUndo(view.history));
//     };
//     const beforeUndoOrRedo = (view) => {
//         clearModality();
//     };
//     const afterUndoOrRedo = (view) => {
//         refreshUndoRedoButtons();
//         savePuzzleState(view);
//     };
//     const undo = (refresh) => {
//         if (refresh === undefined) { refresh = true; }
//         const view = theCurrentPuzzle.view;
//         if (!canUndo(view.history)) { return false; }
//         if (refresh) { beforeUndoOrRedo(view); }
//         view.history.undoCount += 1;
//         view.history.undoCount = clamp(view.history.undoCount, 0, view.history.commands.length);
//         const index = view.history.commands.length - 1 - (view.history.undoCount - 1);
//         const command = view.history.commands[index];
//         genre.undoCommand(view.model, view.state, refresh ? view : undefined, command);
//         if (refresh) { afterUndoOrRedo(view); }
//         statusLine.showText(`Undo ${view.history.commands.length - view.history.undoCount}/${view.history.commands.length}`);
//         return true;
//     };
//     const redo = () => {
//         const view = theCurrentPuzzle.view;
//         if (!canRedo(view.history)) { return false; }
//         beforeUndoOrRedo(view);
//         view.history.undoCount -= 1;
//         view.history.undoCount = clamp(view.history.undoCount, 0, view.history.commands.length);
//         const index = view.history.commands.length - 1 - view.history.undoCount;
//         const command = view.history.commands[index];
//         genre.doCommand(view.model, view.state, view, command);
//         afterUndoOrRedo(view);
//         statusLine.showText(`Redo ${view.history.commands.length - view.history.undoCount}/${view.history.commands.length}`);
//         return true;
//     };

//     const doHint = () => {
//         const view = theCurrentPuzzle.view;
//         if (view === undefined) { return; }
//         hideAllDialogs();
//         scrollPuzzleIntoView();
//         const hint = genre.hint(view.model, view.state, view);
//         savePuzzleState(view);
//         if (hint === undefined) {
//             const check = genre.checkSolved(view.model, view.state, view);
//             if (check.status === "solved") {
//                 statusLine.showText("Press the Check button.");
//             } else {
//                 statusLine.showText("Sorry, no hint is available.");
//                 markHintUsed();
//             }
//         } else {
//             setModalityToHint(hint);
//             statusLine.showText(hint.text);
//             markHintUsed();
//         }
//         refreshPuzzle(view);
//     };
//     const doConfirm = () => { // check if puzzle state matches solution so far (Correct?)
//         const view = theCurrentPuzzle.view;
//         if (view === undefined) { return; }
//         hideAllDialogs();
//         scrollPuzzleIntoView();
//         const check = genre.checkSolved(view.model, view.state, view);
//         clearModality();
//         if (check.status === "solved") {
//             setModalityTo("correct?", "Press the Check button.");
//         } else if (check.compareWithSolution.status === "ok") {
//             setModalityTo("correct?", "Everything is correct so far.");
//         } else {
//             markHintUsed();
//             if (confirm("Something does not match the solution.\n\nUndo until correct?")) {
//                 beforeUndoOrRedo(view);
//                 while (undo(/*refresh=*/false)) {
//                     const check2 = genre.checkSolved(view.model, view.state, view);
//                     if (check2.compareWithSolution.status !== "error") { break; }
//                 }
//                 afterUndoOrRedo(view);
//             } else {
//                 setModalityTo("correct?", "Something does not match the solution.");
//             }
//         }
//         savePuzzleState(view);
//         refreshPuzzle(view);
//     };
//     let timerHandle;
//     const timerPeriod = 100;
//     const refreshTimer = () => {
//         const info = getPuzzleSetInfo(); // TODO:jkd this reads from localStorage. do not poll repeatedly like this.
//         let totalTime = 0;
//         let allSolved = true;
//         let hintUsed = false;
//         info.forEach(it => {
//             if (it.clockTime !== undefined && it.isSolved) {
//                 totalTime += it.clockTime;
//             } else {
//                 allSolved = false;
//             }
//             if (it.hintUsed) {
//                 hintUsed = true;
//             }
//         });
//         timerE.style.visibility = (settingsValues["clock"] === "Show") ? "visible" : "hidden";
//         const mark = "*";
//         const mark1 = theCurrentPuzzle.hintUsed ? mark : "";
//         const mark2 = hintUsed ? mark : "";
//         let s = "";
//         if (allSolved && info.length > 1) {
//              s = `${msToTimeString(theCurrentPuzzle.clockTime)}${mark1} / ${msToTimeString(totalTime)}${mark2}`;
//         } else {
//             s = `${msToTimeString(theCurrentPuzzle.clockTime)}${mark1}`;
//         }
//         // const checkmark = theCurrentPuzzle.isSolved ? "✓" : "";
//         if (theCurrentPuzzle.isSolved) {
//             s += " ✓";
//         }
//         timerE.textContent = s;
//     };
//     const adjustClockTime = (d) => {
//         const view = theCurrentPuzzle.view;
//         if (theCurrentPuzzle.isSolved == false) {
//             theCurrentPuzzle.clockTime += d;
//         }
//         saveDataWithPuzzle(getCurrentPuzzleId(), "clockTime", theCurrentPuzzle.clockTime);
//         refreshTimer();
//     };
//     const tickTimer = () => {
//         adjustClockTime(timerPeriod);
//     };
//     const startTimer = () => {
//         if (timerHandle) {
//             return;
//         }
//         timerHandle = setInterval(tickTimer, timerPeriod);
//     };
//     const stopTimer = () => {
//         if (!timerHandle) {
//             return;
//         }
//         clearInterval(timerHandle);
//         timerHandle = undefined;
//     };
//     const getPuzzleStateLocalStorageKey = (puzzleDesc) => {
//         const puzzleId = genre.getPuzzleId(puzzleDesc);
//         const key = `${genreId}|state|${puzzleId}`;
//         return key;
//     };
//     const getPuzzleHistoryLocalStorageKey = (puzzleDesc) => {
//         const puzzleId = genre.getPuzzleId(puzzleDesc);
//         const key = `${genreId}|history|${puzzleId}`;
//         return key;
//     };
//     let solvedAnimationHandle;
//     const triggerSolvedAnimation = () => {
//         if (!solvedAnimationHandle || solvedAnimationHandle.complete) {
//             solvedAnimationHandle = PUZZLEUTIL.page.startSolvedAnimation(genre.solvedAnimationColors);
//         }
//     };
//     const triggerSolved = () => {
//         theCurrentPuzzle.isSolved = true;
//         saveDataWithPuzzle(getCurrentPuzzleId(), "solved", true);
//         refreshCategoryTabGroupCheckmarks();
//         triggerSolvedAnimation();
//         clearModality();
//         refreshPuzzle(theCurrentPuzzle.view);
//         statusLine.showText("Solved!");
//     };
//     const markHintUsed = () => {
//         if (!theCurrentPuzzle.isSolved) {
//             theCurrentPuzzle.hintUsed = true;
//             saveDataWithPuzzle(getCurrentPuzzleId(), "hintUsed", theCurrentPuzzle.hintUsed);
//         }
//     };
//     const refreshPuzzle = (view) => {
//         genre.refreshView(view);
//     };
//     const goToPuzzle = (startFresh, prevState) => {
//         buttons["new"].textContent = `+${plusCount+1}`;
//         clearModality();
//         const savePuzzleAreaState = () => {
//             window.localStorage.setItem(`${genreId}|dailyPlusTab`, dailyPlusTabGroup.value);
//             window.localStorage.setItem(`${genreId}|categoryTab`, categoryTabGroup.value);
//             window.localStorage.setItem(`${genreId}|plusCount`, `${plusCount}`);
//         };
//         savePuzzleAreaState();
//         const category = categoryTabGroup.value;
//         const dailyPlus = dailyPlusTabGroup.value;
//         const getStateAndHistory = (desc, model, startFresh, prevState) => {
//             const stateKey = getPuzzleStateLocalStorageKey(desc);
//             const historyKey = getPuzzleHistoryLocalStorageKey(desc);
//             const stateString = window.localStorage.getItem(stateKey);
//             const historyString = window.localStorage.getItem(historyKey);
//             if (!startFresh && typeof(stateString) === "string" && typeof(historyString) === "string") {
//                 const state = genre.unstringifyState(model, stateString);
//                 const history = JSON.parse(historyString);
//                 return [state, history];
//             } else {
//                 const state = genre.createInitialState(model, prevState);
//                 const history = {commands: [], undoCount: 0};
//                 return [state, history];
//             }
//         };
//         const setNumber = (dailyPlus === plus) ? plusCount : 0;
//         const desc = hashAndSelectPuzzle(dateString, category, dailyPlus, setNumber);
//         const model = genre.createModel(desc);
//         const [state, history] = getStateAndHistory(desc, model, startFresh, prevState); 
//         const view = genre.createView(model, state);
//         view.desc = desc;
//         view.model = model;
//         view.state = state;
//         view.history = history;
//         view.settingsValues = settingsValues;
//         theCurrentPuzzle.isSolved = false;
//         theCurrentPuzzle.clockTime = 0;
//         if (dailyPlus == plus) {
//             buttons["new"].classList.remove("button-disabled");
//             // buttons["new"].style.display = "";
//             buttons["new"].onclick = (ev) => {
//                 if (confirm("Start a new set of Plus puzzles?")) {
//                     plusCount += 1;
//                     goToPuzzle(/*startFresh=*/true);
//                 }
//             };
//         } else {
//             buttons["new"].classList.add("button-disabled");
//             buttons["new"].onclick = undefined;
//         }
//         buttons["restart"].onclick = (ev) => {
//             if (confirm("Reset the puzzle?")) {
//                 clearModality();
//                 goToPuzzle(/*startFresh=*/true, /*prevState=*/theCurrentPuzzle.view.state);
//                 savePuzzleState(theCurrentPuzzle.view);
//             }
//         };
//         setClickRepeatHandler(buttons["undo"], undo);
//         setClickRepeatHandler(buttons["redo"], redo);
//         buttons["check"].onclick = (ev) => {
//             const view = theCurrentPuzzle.view;
//             if (view === undefined) { return; }
//             const model = view.model;
//             const state = view.state;
//             const check = genre.checkSolved(model, state, view);
//             setModalityToCheck(check);
//             refreshPuzzle(view);
//             savePuzzleState(view);
//             if (check.status === "solved") {
//                 triggerSolved();
//             } else {
//                 if (check.status === "ok") {
//                     statusLine.showText("Seems OK.");
//                 } else if (check.status === "error") {
//                     statusLine.showText("Incorrect.");
//                 } else {
//                     console.error(`unhandled: check.status ${check.status}`);
//                 }
//             }
//         };
//         const doCommandAndWriteToHistory = (view, command) => {
//             if (modality !== "hint") {
//                 clearModality();
//             }
//             genre.doCommand(view.model, view.state, view, command);
//             if (!genre.hideUndoRedoButtons) {
//                 if (view.history.undoCount > 0) {
//                     // truncate history
//                     view.history.commands = view.history.commands.slice(0, -view.history.undoCount);
//                     view.history.undoCount = 0;
//                 }
//                 view.history.commands.push(command);
//                 refreshUndoRedoButtons();
//             }
//             if (genre.enableAutoCheckSolved && !theCurrentPuzzle.isSolved) {
//                 const model = view.model;
//                 const state = view.state;
//                 const checkResult = genre.checkSolved(model, state, view);
//                 if (checkResult.status === "solved") {
//                     triggerSolved();
//                 }
//             }
//             savePuzzleState(view);
//         };
//         view.hooks = { 
//             doCommandAndWriteToHistory, 
//             getPuzzleSetInfo, 
//             clearModality, 
//             setModalityTo,
//             getModality,
//             markHintUsed
//         };
//         refreshPuzzle(view);
//         {
//             const el = pageMiddle.querySelector(".puzzle-div");
//             if (el) { removeElement(el); }
//         }
//         view.root.classList.add("puzzle-div");
//         pageMiddle.appendChild(view.root);
//         document.onkeydown = (ev) => {
//             // global key shortcuts that do not respect focus
//             if (ev.ctrlKey && ev.code === "KeyZ") {
//                 if (ev.shiftKey) {
//                     redo();
//                 } else {
//                     undo();
//                 }
//             }
//             if (ev.ctrlKey && ev.code === "KeyY") {
//                 redo();
//             }
//         };
//         theCurrentPuzzle.view = view;
//         theCurrentPuzzle.isSolved = loadDataWithPuzzle(getCurrentPuzzleId(), "solved", false);
//         theCurrentPuzzle.hintUsed = loadDataWithPuzzle(getCurrentPuzzleId(), "hintUsed", false);
//         theCurrentPuzzle.clockTime = loadDataWithPuzzle(getCurrentPuzzleId(), "clockTime", 0);
//         refreshUndoRedoButtons();
//         refreshTimer();
//         refreshCategoryTabGroupCheckmarks();
//         onPuzzleChange(view);
//     };
//     goToPuzzle();
//     startTimer();
//     const refresh = () => {
//         const view = theCurrentPuzzle.view;
//         refreshPuzzle(view);
//         refreshTimer();
//     };
//     return {
//         refresh,
//         theCurrentPuzzle,
//         markHintUsed,
//         doHint,
//         doConfirm
//     };
// };
// PUZZLEUTIL.page.createStatusLine = () => {
//     const e = createEl({ tag: "div", class: ["status-line"] });
//     let hidden = true;
//     const blankHTML = "&nbsp;"
//     e.innerHTML = blankHTML;
//     const id = `${Math.random()}`;
//     const animator = PUZZLEUTIL.view.createAnimator();
//     const showText = (text) => {
//         if (text === "") { 
//             hide();
//             return;
//         }
//         e.textContent = text;
//         if (!hidden) { return; }
//         hidden = false;
//         shown = true;
//     };
//     const hide = () => {
//         if (hidden) { return; }
//         hidden = true;
//         e.innerHTML = blankHTML;
//     };
//     hide();
//     return {e, showText, hide};
// };
let theSolvedAnimationHandle;
PUZZLEUTIL.page.startSolvedAnimation = (colors) => {
    if (theSolvedAnimationHandle !== undefined && !theSolvedAnimationHandle.complete) {
        // already playing
        return;
    }
    const root = document.getElementById("solved-animation");
    const numStripes = 20;
    root.innerHTML = "";
    const stripes = [];
    for (let i = 0; i < numStripes; ++i) {
        const stripe = document.createElement("div");
        stripes.push(stripe);
        stripe.style.position = "absolute";
        stripe.style.top = `${i * 100 / numStripes}%`;
        stripe.style.left = `0`;
        stripe.style.width = `100%`;
        stripe.style.height = `${100 / numStripes}%`;
        // stripe.style.opacity = "0%";
        root.appendChild(stripe);
    }
    stripes.reverse();

    function sampleKeyframes(keys, time) {
        let sum = 0;
        if (time < 0) {
            return { index1: 0, index2: 0, t: 0 };
        }
        for (let i = 0; i < keys.length - 1; ++i) {
            if (time >= sum && time <= sum + keys[i].dt) {
                return { index1: i, index2: i + 1, t: (time - sum) / keys[i].dt };
            }
            sum += keys[i].dt;
        }
        return { index1: keys.length - 1, index2: keys.length - 1, t: 1, complete: true };
    }

    let timestampStart;
    const timeScale = 4;
    let handle = { complete: false };
    function endAnimation() {
        root.innerHTML = "";
        handle.complete = true;
    }
    function update(timestamp) {
        if (timestampStart == undefined) {
            timestampStart = timestamp;
        }
        let complete = true;
        stripes.forEach((stripe, index) => {
            const startDelay = index * 400 / timeScale;
            const stripeElapsed = (timestamp - timestampStart - startDelay) * timeScale;
            const keys = [{dt: 550, v: 0}, {dt: 500, v: 1}, {dt: 5000, v: 1}, {dt: 1, v: 0}];
            const a = sampleKeyframes(keys, stripeElapsed);
            const v = keys[a.index1].v + (keys[a.index2].v - keys[a.index1].v) * a.t;
            stripe.style.opacity = `${v * 100}%`;
            stripe.style.transform = `scale(1, ${v*2})`;
            // stripe.style.top = `${v*100}`;
            stripe.style.backgroundColor = colors[Math.floor(index) % colors.length];
            if (!a.complete) {
                complete = false;
            }
        });
        if (complete) {
            endAnimation();
        } else {
            requestAnimationFrame(update);
        }
    }
    requestAnimationFrame(update);
    theSolvedAnimationHandle = handle; 
    return handle;
};
