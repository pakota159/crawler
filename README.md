### Installation

Trước hết, để sử dụng crawler kéo dữ liệu về, cần cài đặt một số packages:

`conda install -c conda-forge protego`

`conda install -c conda-forge scrapy`

### Crawl dữ liệu

Hiện tại có 2 bước:

1. Lấy các links blogs về data science

2. Crawl data các đoạn văn bản trong các bài blog trên

Để chạy crawl data các văn bản: `scrapy crawl blog`

### Dữ liệu thô

Hiện tại, có 2 dữ liệu đã kéo về:

1. Simple words: đang lấy ở kaggle, hơn 300000 từ phổ biến (cùng với tần suất xuất hiện của các từ). https://www.kaggle.com/rtatman/english-word-frequency

2. **raw_data.csv**: dữ liệu thô mà mình cần xử lý