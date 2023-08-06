/*
 * potluck.js
 *
 * Javascript support for common potluck server active elements like
 * timers.
 *
 * Must be included as a module and/or with defer.
 */

// jshint esversion: 6
/* global window, document, console, IntersectionObserver */
/* jshint -W097 */
/* jshint -W014 */
/* jshint -W080 */
/* jshint -W040 */

"use strict";

/*--------*
 * Timers *
 *--------*/

// Duration constants in seconds
var ONE_MINUTE = 60;
var ONE_HOUR = 60 * ONE_MINUTE;
var ONE_DAY = 24 * ONE_HOUR;
var ONE_WEEK = 7 * ONE_DAY;

// Milliseconds between timer updates. Timer inaccuracy will be no more
// than half of this value on average.
var TICK_INTERVAL = 500;

function fuzzy_time(seconds) {
    // Converts a number of seconds into a fuzzy time string that rounds
    // to the largest unit (minutes/hours/days/weeks). Ignores the sign
    // of the argument.
    if (seconds < 0) {
        seconds = -seconds;
    }

    // Compute time remaining
    let weeks = seconds / ONE_WEEK;
    let days = (seconds % ONE_WEEK) / ONE_DAY;
    let hours = (seconds % ONE_DAY) / ONE_HOUR;
    let minutes = Math.floor((seconds % ONE_HOUR) / ONE_MINUTE);
    seconds = Math.floor(seconds % ONE_MINUTE);

    if (Math.floor(weeks) > 1) {
        if (weeks % 1 > 0.75) {
            return "almost " + Math.ceil(weeks) + " weeks";
        } else {
            return Math.floor(weeks) + " weeks";
        }
    } else if (Math.floor(weeks) == 1) {
        return Math.floor(7 + days) + " days";
    } else if (Math.floor(days) > 1) {
        if (days % 1 > 0.75) {
            return "almost " + Math.ceil(days) + " days";
        } else {
            return Math.floor(days) + " days";
        }
    } else if (Math.floor(days) == 1) {
        return Math.floor(24 + hours) + " hours";
    } else if (hours > 4) {
        if (hours % 1 > 0.75) {
            return "almost " + Math.ceil(hours) + " hours";
        } else {
            return Math.floor(hours) + " hours";
        }
    } else if (Math.floor(hours) > 0) {
        return Math.floor(hours) + "h " + minutes + "m";
    } else if (minutes > 30) {
        return minutes + " minutes";
    } else if (minutes > 0) {
        let s_str = "" + seconds;
        if (s_str.length == 1) {
            s_str = "0" + s_str;
        }
        return minutes + "m " + s_str + "s";
    } else {
        return seconds + " seconds";
    }
}

// Active countdown timers support
function tick_timer(timer) {
    // Updates the data-time attribute of a countdown timer, and updates
    // the contents of the timer element to display the remaining (or
    // exceeded, if negative) time in appropriate units.

    // Compute new seconds-remaining
    let now = new Date();
    let elapsed_ms = now - timer.last_tick;
    timer.seconds -= elapsed_ms / 1000;
    timer.last_tick = now;

    // Update display
    if (timer.seconds > 0) {
        timer.innerHTML = "(" + fuzzy_time(timer.seconds) + " from&nbsp;now)";
    } else {
        timer.innerHTML = "(" + fuzzy_time(timer.seconds) + " ago)";
    }

    // Reschedule ourselves
    window.setTimeout(tick_timer, TICK_INTERVAL, timer);
}

// Set up callbacks for timers
for (let timer of document.querySelectorAll(".timer")) {
    let seconds = timer.getAttribute("data-time");
    if (seconds == null) {
        continue; // ignore this element
    }
    let seconds_float = parseFloat(seconds);
    if (isNaN(seconds_float)) {
        console.warn(
            "Invalid data-time attribute for a .timer:",
            timer,
            seconds
        );
        continue; // can't process this element
    }
    timer.seconds = seconds_float;
    timer.last_tick = new Date();
    timer.setAttribute("role", "timer"); // ensure ARIA attributes are set
    timer.setAttribute("aria-live", "off");
    tick_timer(timer);
}

/*------------*
 * Validation *
 *------------*/

function validate_task_submit(task_form) {
    // Takes a task form DOM element and runs validation to
    // disable/enable the submit button and add/remove relevant messages.

    let psid = task_form.getAttribute("data-pset");
    let taskid = task_form.getAttribute("data-task");

    let file_browser = task_form.querySelector('input[name="upload"]');
    let time_spent = task_form.querySelector('input[name="time_spent"]');
    let submit_button = task_form.querySelector('input[type="submit"]');

    // If validation is disabled via the global checkbox, or if this task
    // is finalized, skip validation, remove messages, and enable the
    // upload button.
    let task_item = task_form.parentElement.parentElement;
    let pset_item = task_item.parentElement.parentElement;

    let unsubmitted = task_item.classList.contains("unsubmitted");

    let validation_control = document.getElementById("enable_validation");
    if (
        validation_control == null
     || !validation_control.checked
     || pset_item.classList.contains("status-final")
    ) {
        set_validation_messages(task_form, {});
        submit_button.removeAttribute("disabled");
        submit_button.classList.remove("invalid");
        file_browser.removeAttribute("aria-describedby");
        time_spent.removeAttribute("aria-describedby");
        return;
    }

    let filename_label = task_form.querySelectorAll('label')[0];
    let task_filename = filename_label.firstElementChild.innerText.trim();

    // Build an mapping from topics to messages
    let messages = {};

    // Validate the filename
    let current_filename = undefined;
    if (file_browser.files.length > 0) {
        current_filename = file_browser.files[0].name;
    }

    if (current_filename == undefined) {
        current_filename = file_browser.value.split('\\').pop();
    }

    if (current_filename != task_filename) {
        if (unsubmitted) {
            messages.filename = (
                "You must select a file named <code>" + task_filename
              + "</code>"
            );
        } else {
            messages.filename = (
                "To resubmit, select a file named <code>" + task_filename
              + "</code>"
            );
        }
    }

    // Validate the time spent field
    let spent = time_spent.value;

    if (spent == "") {
        if (unsubmitted) {
            messages.time_spent = "You must estimate your time spent.";
        } else {
            messages.time_spent = "To resubmit, estimate your time spent.";
        }
    } else if (isNaN(parseFloat(spent))) {
        messages.time_spent = (
            "Please enter a decimal number of hours (like '0.3', '2', or"
          + " '3.5') for time spent."
        );
    }

    // Set the validation messages
    set_validation_messages(task_form, messages);

    // Enable/disable the upload button
    let file_desc_id = psid + '-' + taskid + '-filename';
    let time_desc_id = psid + '-' + taskid + '-time_spent';
    if (Object.keys(messages).length > 0) {
        submit_button.setAttribute("disabled", true);
        submit_button.classList.add("invalid");
        file_browser.setAttribute("aria-describedby",file_desc_id);
        time_spent.setAttribute("aria-describedby", time_desc_id);
    } else {
        submit_button.removeAttribute("disabled");
        submit_button.classList.remove("invalid");
        file_browser.removeAttribute("aria-describedby");
        time_spent.removeAttribute("aria-describedby");
    }
}

function set_validation_messages(task_form, messages) {
    // Removes any old validation messages for a form and adds new ones.
    // Messages should be a mapping from topics to HTML message strings.

    let psid = task_form.getAttribute("data-pset");
    let taskid = task_form.getAttribute("data-task");

    let task_item = task_form.parentElement.parentElement;
    let msg_list = task_item.querySelector("ul.messages");

    // Remove all old validation messages
    for (let vmsg of msg_list.querySelectorAll("li.validation")) {
        msg_list.removeChild(vmsg);
    }

    // Create and append new validation messages
    for (let msg_topic of Object.keys(messages)) {
        let msg = document.createElement("li");
        msg.classList.add("validation");
        msg.classList.add("topic-" + msg_topic);
        msg.setAttribute("id", psid + '-' + taskid + '-' + msg_topic);
        msg.innerHTML = messages[msg_topic];
        msg_list.appendChild(msg);
    }
}

// Set up form validation
for (let task_form of document.querySelectorAll("form.task_submit")) {
    // Initial validation
    validate_task_submit(task_form);

    for (let input of task_form.querySelectorAll("input")) {
        input.addEventListener(
            "change",
            // jshint -W083
            // task_form is safely per-iteration because it's a for/of
            function () { validate_task_submit(task_form); }
            // jshint +W083
        );
        input.addEventListener(
            "keyup",
            // jshint -W083
            // task_form is safely per-iteration because it's a for/of
            function () { validate_task_submit(task_form); }
            // jshint +W083
        );
    }
}

let validation_switch = document.getElementById("enable_validation");
if (validation_switch != null) {
    validation_switch.addEventListener(
        "change",
        function () {
            // re-validate every task
            for (
                let task_form
             of document.querySelectorAll("form.task_submit")
            ) {
                validate_task_submit(task_form);
            }
        }
    );
}

/*----------------------*
 * Feedback interaction *
 *----------------------*/

let hide_accomplished = document.getElementById("hide_accomplished_goals");
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


/*-------------*
 * Sticky bins *
 *-------------*/

// Global set of currently-floating bins (so that we can manage them as
// multiple tabs)
let FLOATING_BINS = new Set();

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

    let label = bin.querySelector(".bin_label");
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

// Set up for sticky bins:
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

// Returns an ancestor element of the given element that is a sticky bin,
// or null if there is no such ancestor.
function sticky_bin_ancestor(element) {
    if (!element.parentNode) {
        return null;
    } else if (
        element.parentNode.classList
     && element.parentNode.classList.contains("sticky_bin")
   ) {
        return element.parentNode;
    } else {
        return sticky_bin_ancestor(element.parentNode);
    }
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

let TOTAL_FLOATABLE_BINS = bin_index;
