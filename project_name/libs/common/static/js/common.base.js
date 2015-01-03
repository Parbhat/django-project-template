/*global $: false, _: false */
var {{ project_name|upper }} = {{ project_name| upper }} || {};
/* create global namspace for adding functionality,
 * also create a helper function for extending this
 * namespace */
{{ project_name|upper }}.namespace = function (ns_string) {
    "use strict";
    var parts = ns_string.split("."),
        parent = {{ project_name|upper }},
        i;
    // strip redundant leading global
    if (parts[0] === "{{ project_name|upper }}") {
        parts = parts.slice(1);
    }
    for (i = 0; i < parts.length; i += 1) {
        // create a property if it doesn't exist
        if (typeof parent[parts[i]] === "undefined") {
            parent[parts[i]] = {};
        }
        parent = parent[parts[i]];
    }
    return parent;
};

{{ project_name|upper }}.namespace("{{ project_name|upper }}.common");
{{ project_name|upper }}.common.csrf = (function () {
    "use strict";
    /* This code is used to automatically inject the CSRF token into the
     * request header on all non safe (POST, PUT and DELETE) AJAX requests.
     */
    var init = function () {
        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
                }
            }
        });
    },
    csrfSafeMethod = function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    $(function () { init(); });
}());
