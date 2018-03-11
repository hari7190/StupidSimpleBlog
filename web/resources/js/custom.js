/**
 * Created by harims on 3/10/18.
 */

$(document).ready(function () {
    $("#algo-select").on('change', loadAlgo);
});

function loadAlgo(e) {
    $("#algo-div").load("snippets/py-" + e.originalEvent.srcElement.value + ".html", function() {});
    hljs.initHighlighting();
}