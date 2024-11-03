let seconds = 0;
let intervalId;

function startFetching(refreshUrl) {
    
    $('#fetchingModal').modal('show');
    seconds = 0;
    document.getElementById('timer').textContent = seconds;


    intervalId = setInterval(() => {
        seconds++;
        document.getElementById('timer').textContent = seconds;
    }, 1000);

    
    fetch(refreshUrl)  
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            
            updateNews(data);  
            stopFetching();    
        })
        .catch(error => {
            console.error('Fetch error:', error);
            stopFetching(); 
        });
}

function updateNews(newsData) {
    const newsContainer = document.querySelector('.news-container');
    newsContainer.innerHTML = ''; 
    if (newsData.length === 0) {
        newsContainer.innerHTML = '<p>No news available at the moment. Please refresh.</p>';
        return;
    }

    newsData.forEach(news => {
        const newsItem = document.createElement('div');
        newsItem.classList.add('news-item');

        newsItem.innerHTML = `
            <div class="news-title">${news.title || 'No Title'}</div>
            <div class="news-summary">${news.summary || 'No Summary Available'}</div>
            <div><a href="${news.link || '#'}" target="_blank">Read more</a></div>
            <div class="news-date">${news.date || 'Date not available'}</div>
        `;
        newsContainer.appendChild(newsItem);
    });
}

function stopFetching() {
    clearInterval(intervalId); 
    $('#fetchingModal').modal('hide'); 
}


$('#fetchingModal').on('hidden.bs.modal', function () {
    clearInterval(intervalId);
});
