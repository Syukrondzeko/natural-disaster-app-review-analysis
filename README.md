# 🚨 Disaster Mobile App Review Analysis

This project undertakes a comprehensive analysis of user reviews for disaster-related mobile applications from both the Google Play Store and Apple App Store. Aimed at uncovering insights into user sentiments, feature requests, and overall app performance, this analysis is crucial for developers and stakeholders in the disaster management domain.

## 🗂 Dataset Folder Structure

- **phase 0**: Contains lists of apps and their IDs for scraping reviews from the Play Store and App Store.
- **phase 1**: Stores the results of the scraping process.
- **phase 2**: Includes translated non-English reviews.
- **phase 3**: Features a clean dataset after pre-processing, ready for topic modelling.
- **phase 4**: Holds the results of topic modelling, prepared for sentiment analysis.

## 📘 Notebooks

1. **Review Translation**  
   - Translates non-English reviews to English for uniform analysis.
2. **Data Cleansing**  
   - Cleans the dataset to prepare it for topic modelling.
3. **Topic Modelling**  
   - Extracts topics from user reviews using the BERTopic model.
4. **Sentiment Analysis**  
   - Conducts sentiment analysis on user reviews using the VADER tool.

## 📁 src

1. **Apple App Store Scraper**  
   - Scrapes user reviews from Apple App Store apps.
2. **Google Play Store Scraper**  
   - Scrapes user reviews from Google Play Store apps.

## 🙏 Acknowledgements

- Special thanks to the developers and contributors of the [App Store Scraper](https://github.com/cowboy-bebug/app-store-scraper) and [Google Play Scraper](https://github.com/JoMingyu/google-play-scraper) tools, which made this analysis possible.

## 👤 Authors

- [Muhamad Syukron](https://github.com/yourgithubprofile) - Feel free to connect and explore more projects.

---

This project is part of a broader initiative to leverage data science in enhancing disaster preparedness and response strategies. By analyzing user feedback, we aim to contribute valuable insights towards the development of more effective and user-friendly disaster management solutions.
