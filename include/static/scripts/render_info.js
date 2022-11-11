function render_overview(stock_info) {
    html = 
    `<div class="reconissance">
        <div class="co-name co_info">
          <!-- Company name -->
          <h2>${stock_info['company']['companyName']}</h2>
        </div>
        <div class="website co_info">
          <h3>Website</h3>
          <a href="${stock_info['company']['website']}">${stock_info['company']['website']}</a>
        </div>
        <div class="industry co_info">
          <h3>Industry</h3>
          <!-- industry info -->
          <p>${stock_info['company']['industry']}</p>
        </div>
        <div class="description co_info">
          <h3>Description</h3>
          <!-- One or two paras -->
          <p>${stock_info['company']['description']}</p>
        </div>
        <div class="ceo co_info">
          <h2>CEO</h2>
          <h3>${stock_info['company']['CEO']}</h3>
        </div>
        <div class="sector co_info">
          <h3>Sector</h3>
          <p>${stock_info['company']['sector']}</p>
        </div>
    </div>
    `;
    return html;
}


function render_fundamentals(stock_info) {
    html = 
    `<div class="reconissance">
    <div class="co-name co_info">
      <!-- Company name -->
      <h2>${stock_info['company']['companyName']}</h2>
    </div>
    <div class="co_info">
      <b>Time: ${stock_info['quote']['latestTime']}</b>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>Latest Price: </b><p id="latest_price">${stock_info['quote']['latestPrice']}    </p>
        </div>
        <div class="sub-info">
          <b>Previous Price: </b><p id="previous_price">${stock_info['quote']['previousClose']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>Change: </b><p id="change">${stock_info['quote']['change']}    </p>
        </div>
        <div class="sub-info">
          <b>Change %: </b><p id="change_percent">${stock_info['quote']['changePercent']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>High: </b><p id="high">${stock_info['quote']['high']}    </p>
        </div>
        <div class="sub-info">
          <b>Low: </b><p id="low">${stock_info['quote']['low']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>Open: </b><p id="open">${stock_info['quote']['open']}    </p>
        </div>
        <div class="sub-info">
          <b>Close: </b><p id="close">${stock_info['quote']['close']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>Latest Volume:  </b><p id="latest-volume">${stock_info['quote']['latestVolume']}    </p>
        </div>
        <div class="sub-info">
          <b>Previous Volume:  </b><p id="previous-volume">${stock_info['quote']['previousVolume']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>Week 52 high:  </b><p id="high52">${stock_info['quote']['week52High']}    </p>
        </div>
        <div class="sub-info">
          <b>Week 52 low:  </b><p id="low52">${stock_info['quote']['week52Low']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <div class="flex-box">
        <div class="sub-info">
          <b>Total Volume:  </b><p id="total-volume">${stock_info['quote']['volume']}    </p>
        </div>
        <div class="sub-info">
          <b>Average Total Volume:  </b><p id="avg-vol">${stock_info['quote']['avgTotalVolume']}    </p>
        </div>
      </div>
    </div>
    <div class="co_info">
      <b>Market Cap: ${stock_info['quote']['marketCap']}</b>
    </div>
    <div class="co_info">
      <b>Currency: ${stock_info['quote']['currency']}</b>
    </div>
    <div class="co_info">
      <b>Primary Exchange: ${stock_info['quote']['primaryExchange']}</b>
    </div>
  </div>`
  return html;
}

function render_news(stock_info) {
  news = stock_info['news'];
  news_item = '';
  for (var n in news) {
    var date = new Date(news[n]['datetime'])
    data = `
    <div class="news">
      <div class="headline">
        <h1>${ news[n]["headline"] }</h1>
      </div>
      <div class="source">
        <p>Posted by ${ news[n]['source'] } at ${ date.toLocaleString() }</p>
      </div>
      <div class="link">
        <a href="${ news[n]['url'] }">Source</a>
      </div>
      <div class="summary">
        <p>${ news[n]['summary'] }</p>
      </div>
      <div class="image">
        <img src="${ news[n]['image'] }" alt="">
      </div>
    </div>
    \n`;
    news_item += data;
  }
  html = `
  <div class='reconissance'>
    ${news_item}
  </div>
  `;
  return html;
}