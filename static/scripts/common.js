//set svg viewbox size
$("svg").each(function() {
    this.setAttribute("viewBox", "0 0 " + $(this).parent().width() + " " + $(this).parent().height());
});