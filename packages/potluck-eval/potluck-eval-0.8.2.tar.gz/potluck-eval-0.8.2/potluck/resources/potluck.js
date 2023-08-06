var CODEFOCUS = null;

function transition(id, classA, classB) {
    let node = document.getElementById(id);
    if (node) {
        node.className = node.className.replace(classA, classB);
    }
}

function toggle(id, classA, classB, toggle_id, on_symbol, off_symbol) {
    let node = document.getElementById(id);
    let toggle_node = document.getElementById(toggle_id);
    if (on_symbol == undefined) { on_symbol = "&nbsp;&ndash;&nbsp;"; }
    if (off_symbol == undefined) { off_symbol = "&nbsp;+&nbsp;"; }
    if (node) {
        if (node.className.includes(classA)) {
            node.className = node.className.replace(classA, classB);
            if (toggle_node) {
                toggle_node.innerHTML = off_symbol;
            }
            return classB;
        } else if (node.className.includes(classB)) {
            node.className = node.className.replace(classB, classA);
            if (toggle_node) {
                toggle_node.innerHTML = on_symbol;
            }
            return classA;
        }
    }
    return null;
}

function unfocusCodeLine() {
    if (CODEFOCUS) {
        transition(CODEFOCUS, "codeline_focus", "codeline_plain");
    }
    CODEFOCUS = null;
}

function focusCodeLine(codeid, lineid) {
    unfocusCodeLine();
    transition(codeid, "hide", "show");
    transition(lineid, "codeline_plain", "codeline_focus");
    CODEFOCUS = lineid;
}

function toggleCodeLine(id, toggle_id, on_symbol, off_symbol) {
    let status = toggle(
        id,
        "codeline_closed",
        "codeline_open",
        toggle_id,
        on_symbol,
        off_symbol
    );
    toggle(id + "_refs", "show", "hide");
    // focusCodeLine(id);
}

function openCodeLine(codeid, lineid, toggle_id, on_symbol) {
    transition(codeid, "hide", "show");
    if (on_symbol == undefined) { on_symbol = "&nbsp;&ndash;&nbsp;"; }
    
    let line = document.getElementById(lineid);
    let toggle_elem = document.getElementById(toggle_id);
    if (
        !line.className.includes("codeline_none")
     && (
            line.className.includes("codeline_closed")
         || line.className.includes("codeline_open")
        )
    ) {
        line.className = line.className.replace(
            "codeline_closed",
            "codeline_open"
        );
        if (toggle_elem) {
            toggle_elem.innerHTML = on_symbol;
        }
        transition(lineid + "_refs", "hide", "show");
    }
    focusCodeLine(codeid, lineid);
}

function toggleSection(id, toggle_id, on_symbol, off_symbol) {
    toggle(id, "show", "hide", toggle_id, on_symbol, off_symbol);
}

function toggleRow(id, toggle_id, on_symbol, off_symbol) {
    // Either might be missing, but if either toggles, so should the symbol
    // (it won't toggle twice since it detects the show/hide destination state)
    toggle("row_" + id, "show", "hide", toggle_id, on_symbol, off_symbol);
    toggle("ul_" + id, "show", "hide", toggle_id, on_symbol, off_symbol);
}

function openRow(sectionid, id, toggle_id, on_symbol) {
    transition(sectionid, "hide", "show");
    transition("row_" + id, "hide", "show");
    transition("ul_" + id, "hide", "show");

    if (on_symbol == undefined) { on_symbol = "&nbsp;&ndash;&nbsp;"; }
    let the_toggle = document.getElementById(toggle_id);
    if (the_toggle) {
        the_toggle.innerHTML = on_symbol;
    }
}    

function zoom(id) {
    toggle(id, "img_small", "img_large");
}

function toggleClass(classs, classA, classB) {
    let list = document.getElementsByClassName(classs);
    for (var i = 0; i < list.length; i++) {
        if (list[i].className.includes(classA)) {
            list[i].className = list[i].className.replace(classA, classB);
        } else if (list[i].className.includes(classB)) {
            list[i].className = list[i].className.replace(classB, classA);
        }
    }
    return null;
}

function togglePoints() {
    toggleClass("autoreport_points", "points_hide", "show");
    toggleClass("regrade", "regrade_hide", "regrade_show");
}


function toggleTab() {
    // Click event handler for anchors in a tabs setup to hide all other
    // tabs except the one that corresponds to the one we clicked on.
    let thistab = event.currentTarget;
    let tabstop = thistab.parentElement;
    let tabbed = tabstop.parentElement;
    let tabsbot = tabbed.querySelector(".tabs-bot");
    let index = Array.prototype.indexOf.call(tabstop.children, thistab);
    let thiscontent = tabsbot.children[index];
    if (thistab.classList.contains("selected")) {
        thiscontent.classList.remove("selected");
        thistab.classList.remove("selected");
        thistab.removeAttribute("aria-current");
    } else {
        thiscontent.classList.add("selected");
        thistab.classList.add("selected");
        thistab.setAttribute("aria-current", "true");
        thistab.setAttribute("aria-expanded", "true");
        thiscontent.removeAttribute("aria-hidden");
    }

    // If we opened it:
    if (thistab.classList.contains("selected")) {
        // de-select all other tabs
        for (let tab of tabstop.children) {
            if (tab != thistab) {
                tab.classList.remove("selected");
                tab.removeAttribute("aria-current");
                tab.removeAttribute("aria-expanded");
            }
        }
        // hide all other tab content
        for (let content of tabsbot.children) {
            if (content != thiscontent) {
                content.classList.remove("selected");
                content.setAttribute("aria-hidden", "true");
            }
        }
    }
}


/*----------------------*
 * Feedback interaction *
 *----------------------*/

window.addEventListener("load", function () {
    let hide_accomplished = document.getElementById("hide_accomplished_goals")
    if (hide_accomplished != null) {
        hide_accomplished.addEventListener(
            "change",
            function () {
                if (hide_accomplished.checked) {
                    for (
                        let row
                     of document.querySelectorAll(
                         "div.rubric_row.status_accomplished:not(.tag_category)"
                        )
                    ) {
                        row.style.display = "none";
                    }
                } else {
                    for (
                        let row
                     of document.querySelectorAll(
                         "div.rubric_row.status_accomplished:not(.tag_category)"
                        )
                    ) {
                        row.style.display = "block";
                    }
                }
            }
        );
    }
});


/*-------------*
 * Sticky bins *
 *-------------*/

// Global set of currently-floating bins (so that we can manage them as
// multiple tabs)
var FLOATING_BINS = new Set();

// Defaults for observation are to observe relative to viewport with a 0%
// threshold, which is what we want.
let observer = new IntersectionObserver(function (entries) {
    for (let entry of entries) {
        let binContent = entry.target.querySelector(".sticky_bin");
        if (entry.isIntersecting) {
            // This bin's context is in view, so the bin content should snap
            // into the context.
            stop_floating(binContent); // before CSS class changes
        } else {
            // This bin's context is now just out of view, so the bin content
            // should snap into its floating state
            start_floating(binContent); // before CSS class changes
            binContent.classList.remove("sticky_inplace");
            binContent.classList.add("sticky_floating");
        }
    }
});

/*
 * Detach the given bin (content) from its context and start floating it.
 */
function start_floating(bin) {
    // Measure current bin content height and set the height of its
    // parent so that while it floats the parent doesn't shrink
    let context = bin.parentElement;
    let current_content_height = bin.getBoundingClientRect().height;
    context.style.height = current_content_height + "px";

    // Are any other bins maximized now?
    let other_maximized = false;
    for (let bin of FLOATING_BINS) {
        if (bin.classList.contains("sticky_maximized")) {
            other_maximized = true;
            break;
        }
    }

    // Add to our floating bins set
    FLOATING_BINS.add(bin);

    // Remember maximized state
    if (bin.wasMaximized && !other_maximized) {
        bin.classList.add("sticky_maximized");
    } else {
        bin.classList.add("sticky_minimized");
    }

    // Set floating/inplace class status
    bin.classList.add("sticky_floating");
    bin.classList.remove("sticky_inplace");

    // Rearrange all floating bins
    rearrange_floating_bins();

    // Set the scrollTop if we've got a saved value for that
    if (bin.scrollTopMemory) {
        bin.scrollTop = bin.scrollTopMemory;
    }
}

/*
 * Stop floating the given bin (content). Purges CSS properties so that
 * they can revert to 
 */
function stop_floating(bin) {
    // First, measure the current scroll position of the page overall
    let scroll_now = document.body.parentElement.scrollTop;

    // revert to natural height
    let context = bin.parentElement;
    context.style.height = "";

    // Remember scroll top value and open/closed state
    bin.scrollTopMemory = bin.scrollTop;
    bin.scrollTop = 0;
    bin.wasMaximized = bin.classList.contains("sticky_maximized");

    // remove from floating bins set
    FLOATING_BINS.delete(bin);

    // undo fixed styles
    bin.style.removeProperty("position");
    bin.style.removeProperty("top");
    bin.style.removeProperty("left");
    bin.style.removeProperty("right");
    bin.style.removeProperty("bottom");
    bin.style.removeProperty("width");
    bin.style.removeProperty("height");

    let label = bin.querySelector(".bin_label")
    label.style.removeProperty("position");
    label.style.removeProperty("top");
    label.style.removeProperty("left");
    label.style.removeProperty("right");
    label.style.removeProperty("bottom");
    label.style.removeProperty("width");
    label.style.removeProperty("height");
    label.style.removeProperty("transform");

    // Set floating/inplace class status
    bin.classList.remove("sticky_floating");
    bin.classList.add("sticky_inplace");

    bin.classList.remove("sticky_maximized");
    bin.classList.remove("sticky_minimized");

    // Rearrange all floating bins
    rearrange_floating_bins();


    // Finally, re-set the scroll_now value, but only after we let other
    // events flush and finish
    // TODO: This breaks click-on-scrollbar-to-jump when jumping in a way
    // that un-floats a bin... for now, we'll just live with that.
    window.setTimeout(
        function () { document.body.parentElement.scrollTop = scroll_now; },
        0
    );
}

/*
 * Rearranges the currently-floating bins so that they don't overlap each
 * other. Note that because we're using a no-DOM-changes technique, we
 * cannot accommodate an arbitrary number of floating bins, so it's up to
 * you the user of this code to make sure that there aren't enough bins
 * to make things too crowded. Basically, each floating bin gets 1/N of
 * the either vertical or horizontal space for its title, and when
 * expanded, bins take up 50% of the other axis.
 */
function rearrange_floating_bins() {
    let n_bins = FLOATING_BINS.size;
    let each_pct = Math.round(100 / n_bins);

    // Figure out if any bins are maximized
    let any_maximized = false;
    for (let bin of FLOATING_BINS) {
        if (bin.classList.contains("sticky_maximized")) {
            any_maximized = true;
        }
    }

    // Set positioning of each bin
    let in_order = Array.from(FLOATING_BINS);
    in_order.sort((a, b) => a.bin_number - b.bin_number);
    let pct_sofar = 0;
    for (let bin of in_order) {
        // Reference to the bin label
        let label = bin.querySelector(".bin_label");

        // clear out previous properties so we don't have contradictions
        bin.style.removeProperty("position");
        bin.style.removeProperty("top");
        bin.style.removeProperty("bottom");
        bin.style.removeProperty("left");
        bin.style.removeProperty("right");
        bin.style.removeProperty("width");
        bin.style.removeProperty("height");

        label.style.removeProperty("position");
        label.style.removeProperty("top");
        label.style.removeProperty("bottom");
        label.style.removeProperty("left");
        label.style.removeProperty("right");
        label.style.removeProperty("width");
        label.style.removeProperty("height");

        if (bin.classList.contains("sticky_maximized")) {
            // if maximized, take up bottom 50% of screen
            bin.style.width = "100%";
            bin.style.height = "50%";
            bin.style.bottom = "0pt";
            bin.style.left = "0pt";
            // also grab label and pull it out
            label.style.position = "fixed";
            label.style.bottom = "50%";
            label.style.left = pct_sofar + "%";
            label.style.width = each_pct + "%";
        } else {
            // if minimized, appear along top of maximized area OR
            // along bottom of screen (if nothing is maximized)
            bin.style.width = each_pct + "%";
            bin.style.left = pct_sofar + "%";
            if (any_maximized) {
                bin.style.bottom = "50%";
            } else {
                bin.style.bottom = "0pt";
            }
        }
        

        // Update pct_sofar
        pct_sofar += each_pct;
    }
}

// Toggles a bin between minimized and maximized states
function show_or_hide_my_parent() {
    toggle_bin_state(this.parentElement);
}

// Toggles a floating sticky bin's state. If a second parameter is
// supplied and it's true or false, true forces maximization and false
// forces minimization. Does nothing if the bin is not currently
// floating.
function toggle_bin_state(bin, maximize) {
    if (!bin.classList.contains("sticky_floating")) {
        return;
    }

    if (maximize == undefined) {
        maximize = true;
        if (bin.classList.contains("sticky_maximized")) {
            maximize = false;
        }
    }

    // first minimize ALL floating bins
    for (let other_bin of FLOATING_BINS) {
        // Remember scroll position as we minimize
        if (other_bin.classList.contains("sticky_maximized")) {
            other_bin.scrollTopMemory = other_bin.scrollTop;
        }
        other_bin.classList.remove("sticky_maximized");
        other_bin.classList.add("sticky_minimized");
    }

    // Now maximize this bin if we're maximizing
    if (maximize) {
        bin.classList.add("sticky_maximized");
        bin.classList.remove("sticky_minimized");
    }

    // rearrange all floating bins based on the new state
    rearrange_floating_bins();

    if (maximize && bin.scrollTopMemory) {
        bin.scrollTop = bin.scrollTopMemory;
    }
}


// Ensures that a specific sticky bin is currently visible, either by
// maximizing it if it's floating, or doing nothing if it's not floating.
function ensure_bin_is_visible(bin) {
    if (bin.classList.contains("sticky_floating") && !bin.classList.contains("sticky_maximized")) {

    }
}

// Returns an ancestor element of the given element that is a sticky bin,
// or null if there is no such ancestor.
function sticky_bin_ancestor(element) {
    if (!element.parentNode || !element.parentNode.classList) {
        return null;
    } else if (element.parentNode.classList.contains("sticky_bin")) {
        return element.parentNode;
    } else {
        return sticky_bin_ancestor(element.parentNode);
    }
}

var TOTAL_FLOATABLE_BINS;

// Set up for sticky bins:
window.addEventListener("load", function () {
    let bin_index = 0;
    for (let context of document.querySelectorAll(".sticky_context")) {
        // Observe each sticky bin context
        observer.observe(context);

        // Number each bin in source order
        context.querySelector(".sticky_bin").bin_number = bin_index;
        bin_index += 1;

        // Add minimize/maximize handlers to bin labels
        let bin_label = context.querySelector(".bin_label");
        bin_label.addEventListener("click", show_or_hide_my_parent);
        bin_label.setAttribute(
            "aria-label",
            (
                "Activate to make this section more prominent, or again to"
              + " hide it (unless scrolled into view already)."
            )
        );
    }

    // Find all links that link to anchors and ensure that when we click
    // them before we jump, if they link to an anchor that's in a sticky
    // bin, we maximize that sticky bin if it's floating
    for (let link of document.querySelectorAll("a:link")) {
        // only look at anchor links
        let bare_url = (
            window.location.protocol
          + "//"
          + window.location.host
          + window.location.pathname
        );
        let link_href = link.href;
        let link_hash = link.hash;
        if (link_href.startsWith(bare_url) && link_hash.length > 0) {
            let destination = document.getElementById(link_hash.substring(1));
            if (!destination) {
                console.warn("Broken # link:", link);
                continue; // broken link I guess
            }

            let bin = sticky_bin_ancestor(destination); // let is critical here!
            if (bin != null) {
                // If the destination's in a sticky bin, add a click handler
                // to the link to open that bin
                link.addEventListener("click", function () {
                    toggle_bin_state(bin, true);
                    return true; // continue with normal event operation
                });
            }
        }
    }

    TOTAL_FLOATABLE_BINS = bin_index;
});
