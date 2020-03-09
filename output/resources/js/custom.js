/**
 * Created by harims on 3/10/18.
 */

/*********************
*   Event Listeners  *
 ********************/

$(document).ready(function () {
    $("#algo-select").on('change', loadAlgo);
});


/*********************
 *   AJAX Tasks   *
 ********************/

function loadAlgo(e) {

    toogleCodeContainer(false);

    $("#algo-div").load("snippets/py-" + e.originalEvent.srcElement.value + ".html", function (responseText, textStatus, req) {
        if (textStatus == "error") {
            $("#algo-div").html('#TBD');
        } else {
            codeHighlight();
        }
    });

    toogleCodeContainer(true);
}

/*********************
 *   DOM Tasks   *
 ********************/

function toogleCodeContainer(show) {
    if(show)
        $("#code-container").removeClass('not-visible').addClass('visible');
    else
        $("#code-container").removeClass('visible').addClass('not-visible');
}


function codeHighlight(){
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });
}