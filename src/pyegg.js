(function(){
"use strict";
function ՐՏ_Iterable(iterable) {
    var tmp;
    if (iterable.constructor === [].constructor || iterable.constructor === "".constructor || (tmp = Array.prototype.slice.call(iterable)).length) {
        return tmp || iterable;
    }
    if (Set && iterable.constructor === Set) {
        return Array.from(iterable);
    }
    return Object.keys(iterable);
}

(function(){

    var __name__ = "__main__";

    function hola() {
        document.getElementById("result").innerHTML = "hola";
    }
})();
})();