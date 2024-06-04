function validateSearch() {
    var query = document.getElementById('search-input').value.trim();
    if (query === '') {
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#search-input');
    const searchButton = document.querySelector('.search-button'); 

    searchButton.addEventListener('click', function(event) {
        if (window.innerWidth <= 768) { 
            if (searchInput.style.display === 'none' || searchInput.style.display === '') {
                searchInput.style.display = 'block'; 
                searchInput.focus(); 
            } else {
                searchInput.style.display = 'none'; 
            }
        }
    });

    searchInput.addEventListener('keyup', function() {
        const query = searchInput.value.trim();
        
        fetch(`/search/?q=${query}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.text())
        .then(data => {
            const mediaContainer = document.querySelector('#media-container');
            mediaContainer.innerHTML = data;
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
    });
});

$(document).ready(function() {
    $('#search-input').keyup(function() {
        let query = $(this).val();
        
        if (query.length >= 3) {  
            $.ajax({
                url: '/search-suggestions/',
                data: {
                    'term': query
                },
                dataType: 'json',
                success: function(data) {
                    let suggestions = data.map(item => `<li>${item}</li>`).join('');
                    $('#search-suggestions').html(suggestions).show();
                },
                error: function(error) {
                    console.log('Error fetching suggestions:', error);
                }
            });
        } else {
            $('#search-suggestions').hide();
        }
    });
    
});

