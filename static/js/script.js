function myFunc() {
    var navbar = document.getElementById('nav');
    navbar.classList.toggle('show');
    
    // Check if nav is visible
    if(navbar.classList.contains('show')) {
        //to add event listener to close nav when clicking outside
        document.addEventListener('click', closeNavOnClickOutside);
    } else {
        // to remove event listener to close nav when clicking outside
        document.removeEventListener('click', closeNavOnClickOutside);
    }
}

function closeNavOnClickOutside(event) {
    var navbar = document.getElementById('nav');
    var toggleBtn = document.querySelector('.toggle-btn');

    if (!navbar.contains(event.target) && !toggleBtn.contains(event.target)) {
        navbar.classList.remove('show');
        document.removeEventListener('click', closeNavOnClickOutside);
    }
}
$(document).ready(function(){
    $('#search-form').on('submit', function(event){
        event.preventDefault();
        var query = $(this).find('input[name="q"]').val();
        $.ajax({
            url: $(this).attr('action'),
            type: 'GET',
            data: { 'q': query },
            success: function(response){
                $('#search-results').html(response);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});
$(document).ready(function(){
    console.log("Autocomplete script loaded");  

    $("#search-input").autocomplete({
        source: function(request, response) {
            console.log("Autocomplete request for:", request.term);  
            
            $.ajax({
                url: "{% url 'autocomplete_search' %}",
                type: 'GET',
                data: { 'q': request.term },
                dataType: 'json',
                success: function(data) {
                    console.log("Received suggestions:", data.suggestions);  
                    response(data.suggestions);
                },
                error: function(error){
                    console.log("Error:", error);
                }
            });
        },
        minLength: 2
    });
});
