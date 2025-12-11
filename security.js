/**
 * SECURITY SCRIPT
 * Implements anti-theft measures and disables developer tools shortcuts.
 */

(function() {
    'use strict';

    // 1. Disable Right Click
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });

    // 2. Disable Dragging Images
    document.addEventListener('dragstart', function(e) {
        if (e.target.tagName === 'IMG') {
            e.preventDefault();
            return false;
        }
    });

    // 3. Disable Keyboard Shortcuts (F12, Ctrl+U, Ctrl+Shift+I, etc.)
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.key === 'F12' || e.keyCode === 123) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+I (DevTools)
        if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.keyCode === 73)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+C (Inspect Element)
        if (e.ctrlKey && e.shiftKey && (e.key === 'C' || e.key === 'c' || e.keyCode === 67)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+J (Console)
        if (e.ctrlKey && e.shiftKey && (e.key === 'J' || e.key === 'j' || e.keyCode === 74)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+U (View Source)
        if (e.ctrlKey && (e.key === 'U' || e.key === 'u' || e.keyCode === 85)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+S (Save)
        if (e.ctrlKey && (e.key === 'S' || e.key === 's' || e.keyCode === 83)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+P (Print)
        if (e.ctrlKey && (e.key === 'P' || e.key === 'p' || e.keyCode === 80)) {
            e.preventDefault();
            return false;
        }
    });

    // 4. Console Disclaimer (for those who open it anyway via menu)
    console.log("%cSTOP!", "color: red; font-size: 50px; font-weight: bold; -webkit-text-stroke: 1px black;");
    console.log("%cThis is a portfolio site. The code is proprietary.", "font-size: 20px;");

})();
