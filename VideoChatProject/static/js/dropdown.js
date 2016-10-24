
var options = [];

$( '.dropdown-menu a' ).on( 'click', function( event ) {
    var form_big = document.forms[1];

   var $target = $( event.currentTarget ),
       val = $target.attr( 'data-value' ),
       $inp = $target.find( 'input' ),
       idx;

   if ( ( idx = options.indexOf( val ) ) > -1 ) {
      options.splice( idx, 1 );
       var inputs = form_big.children;
       for (var i = 0; i < inputs.length; ++i)
           if (inputs[i].value == val) {
               form_big.removeChild(inputs[i]);
           }

      setTimeout( function() { $inp.prop( 'checked', false ) }, 0);
   } else {
      options.push( val );
       var input = document.createElement('input');
       input.type = 'hidden';
       input.name = "models";
       input.value = val;
       form_big.appendChild(input);

      setTimeout( function() { $inp.prop( 'checked', true ) }, 0);
   }

   $( event.target ).blur();
      
   console.log( options );
   return false;
});