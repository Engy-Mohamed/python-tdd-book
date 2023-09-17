var initialize = function (){  
    console.log('inialize 1') ; 
$('input[name="text"]').on('keypress', function(){
    $('.has-error').hide();
});
};
