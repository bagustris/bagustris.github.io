/* ==========================================================================
   Various functions that we want to use within the template
   ========================================================================== */

import { plotlyDarkLayout, plotlyLightLayout } from './theme.js';

// Determine the expected state of the theme toggle, which can be "dark", "light", or
// "system". Default is "system".
let determineThemeSetting = () => {
  let themeSetting = localStorage.getItem("theme");
  return (themeSetting != "dark" && themeSetting != "light" && themeSetting != "system") ? "system" : themeSetting;
};

// Determine the computed theme, which can be "dark" or "light". If the theme setting is
// "system", the computed theme is determined based on the user's system preference.
let determineComputedTheme = () => {
  let themeSetting = determineThemeSetting();
  if (themeSetting != "system") {
    return themeSetting;
  }
  return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
};

// detect OS/browser preference
const browserPref = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

// Set the theme on page load or when explicitly called
let setTheme = (theme) => {
  const user_pref_theme = theme || localStorage.getItem("theme") || $("html").attr("data-theme");
  let use_theme = user_pref_theme || browserPref;

  // Force light theme on mobile if no user preference is set
  if (!user_pref_theme && $(window).width() < 925) {
    use_theme = "light";
  }

  if (use_theme === "dark") {
    $("html").attr("data-theme", "dark");
    $("#theme-icon").removeClass("fa-sun").addClass("fa-moon");
  } else {
    $("html").removeAttr("data-theme");
    $("#theme-icon").removeClass("fa-moon").addClass("fa-sun");
  }
};

// Toggle the theme manually
var toggleTheme = () => {
  const current_theme = $("html").attr("data-theme");
  const new_theme = current_theme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", new_theme);
  setTheme(new_theme);
};

/* ==========================================================================
   Greedy Navigation
   ========================================================================== */

var $nav = $("#site-nav");
if ($nav.length > 0) {
  var $btn = $("#site-nav button");
  var $vlinks = $("#site-nav .visible-links");
  var $vlinks_persist_tail = $vlinks.children("*.persist.tail");
  var $hlinks = $("#site-nav .hidden-links");

  var breaks = [];

  function updateNav() {
    var availableSpace = $btn.hasClass("hidden") ? $nav.width() : $nav.width() - $btn.width() - 30;

    // The visible list is bigger than the available space
    if ($vlinks.width() > availableSpace) {
      // Record the width of the list
      breaks.push($vlinks.width());

      // Move item to the hidden list
      $vlinks.children("*:not(.persist)").last().prependTo($hlinks);

      // Show the dropdown btn
      if ($btn.hasClass("hidden")) {
        $btn.removeClass("hidden");
      }

      // The visible list is still bigger than the available space
      if ($vlinks.width() > availableSpace) {
        updateNav();
      }

      // The visible list is smaller than the available space
    } else {
      // Check if there is space for another item in the nav
      if (availableSpace > breaks[breaks.length - 1]) {
        // Move the item to the visible list
        if ($vlinks_persist_tail.length > 0) {
          $hlinks.children().first().insertBefore($vlinks_persist_tail);
        } else {
          $hlinks.children().first().appendTo($vlinks);
        }
        breaks.pop();
      }

      // Hide the dropdown btn if hidden list is empty
      if (breaks.length < 1) {
        $btn.addClass("hidden");
        $hlinks.addClass("hidden");
        $btn.removeClass("close");
      }
    }

    // Keep focus on dropdown btn
    $btn.attr("count", breaks.length);

    // Update the padding on the body so that the content is not hidden by the masthead
    var mastheadHeight = $(".masthead").height();
    $("body").css("padding-top", mastheadHeight + "px");

    // For the side-bar on large screens, add some padding
    if ($(".author__urls-wrapper button").is(":visible")) {
      $(".sidebar").css("padding-top", "");
    } else {
      $(".sidebar").css("padding-top", mastheadHeight + "px");
    }
  }

  $(window).on("resize", function () {
    updateNav();
  });

  if (screen.orientation) {
    screen.orientation.addEventListener("change", function () {
      updateNav();
    });
  }

  $btn.on("click", function () {
    $hlinks.toggleClass("hidden");
    $(this).toggleClass("close");
  });

  updateNav();
}

/* ==========================================================================
   Plotly integration script so that Markdown codeblocks will be rendered
   ========================================================================== */

// Read the Plotly data from the code block, hide it, and render the chart as new node. This allows for the 
// JSON data to be retrieve when the theme is switched. The listener should only be added if the data is 
// actually present on the page.
let plotlyElements = document.querySelectorAll("pre>code.language-plotly");
if (plotlyElements.length > 0) {
  document.addEventListener("readystatechange", () => {
    if (document.readyState === "complete") {
      plotlyElements.forEach((elem) => {
        // Parse the Plotly JSON data and hide it
        var jsonData = JSON.parse(elem.textContent);
        elem.parentElement.classList.add("hidden");

        // Add the Plotly node
        let chartElement = document.createElement("div");
        elem.parentElement.after(chartElement);

        // Set the theme for the plot and render it
        const theme = (determineComputedTheme() === "dark") ? plotlyDarkLayout : plotlyLightLayout;
        if (jsonData.layout) {
          jsonData.layout.template = (jsonData.layout.template) ? { ...theme, ...jsonData.layout.template } : theme;
        } else {
          jsonData.layout = { template: theme };
        }
        Plotly.react(chartElement, jsonData.data, jsonData.layout);
      });
    }
  });
}

/* ==========================================================================
   Actions that should occur when the page has been fully loaded
   ========================================================================== */

$(document).ready(function () {
  // SCSS SETTINGS - These should be the same as the settings in the relevant files 
  const scssLarge = 925;          // pixels, from /_sass/_themes.scss
  const scssMastheadHeight = 70;  // pixels, from the current theme (e.g., /_sass/theme/_default.scss)

  // If the user hasn't chosen a theme, follow the OS preference
  setTheme();
  window.matchMedia('(prefers-color-scheme: dark)')
        .addEventListener("change", (e) => {
          if (!localStorage.getItem("theme")) {
            setTheme(e.matches ? "dark" : "light");
          }
        });

  // Enable the theme toggle
  $('#theme-toggle').on('click', toggleTheme);

  // Enable the sticky footer
  var bumpIt = function () {
    if ($(".page__footer").length > 0) {
      $("body").css("margin-bottom", $(".page__footer").outerHeight(true));
    }
  }
  $(window).resize(function () {
    didResize = true;
  });
  setInterval(function () {
    if (didResize) {
      didResize = false;
      bumpIt();
    }}, 250);
  var didResize = false;
  bumpIt();

  // FitVids init
  if (typeof fitvids === 'function') fitvids();

  // Follow menu drop down
  $(".author__urls-wrapper button").on("click", function () {
    $(".author__urls").fadeToggle("fast", function () { });
    $(".author__urls-wrapper button").toggleClass("open");
  });

  // Restore the follow menu if toggled on a window resize
  jQuery(window).on('resize', function () {
    if ($('.author__urls.social-icons').css('display') == 'none' && $(window).width() >= scssLarge) {
      $(".author__urls").css('display', 'block')
    }
  });

  // Init smooth scroll, this needs to be slightly more than then fixed masthead height
  if ($.fn.smoothScroll) {
    $("a").smoothScroll({
      offset: -scssMastheadHeight,
      preventDefault: false,
    });
  }

});
