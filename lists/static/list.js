window.superLists = {}
window.superLists.initialize = function (){   
$('input[name="text"]').on('keypress', function(){
    $('.has-error').hide();
});
};
