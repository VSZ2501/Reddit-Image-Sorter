# **README.md**

## **Reddit Image Sorter**

Reddit Image Sorter is a Python application with a graphical user interface (GUI) designed to automatically sort images (JPEG, PNG, GIF) into folders corresponding to selected subreddits. The application leverages `tkinter` for the GUI and additional libraries for image processing.

---

## **Features**

- **Image Display**:
  - Randomly displays images from the selected source folder.
  - Handles GIF files with frame-by-frame animation.
  - Shows the file name and its size in megabytes (MB).

- **Image Sorting**:
  - Sorts images into folders corresponding to the selected subreddits.
  - Renames images using the format: `name_[subreddit]_date.extension`.
  - Automatically creates folders for each selected subreddit.

- **User-Friendly Interface**:
  - Displays subreddit categories with details (members, posts per day, specifics).
  - Easy navigation with a scrollable list of subreddits.
  - Button to dynamically change the source folder for images.

---

## **Prerequisites**

Ensure you have the required dependencies installed before running the script.

### **Dependencies**
- Python 3.8 or later
- Python Libraries:
  - `tkinter` (included by default with Python)
  - `Pillow` (for image processing)
  
To install `Pillow`, run:
```bash
pip install pillow
```

### **Required Files**
- **subreddit_list.txt**: A text file containing subreddit information.
  - Expected format:
    ```
    [CATEGORY]Category Name
    Subreddit Name, Number of Members, Posts/24h, Specific Details
    ```

---

## **How to Use**

### **1. Launch the Application**
Run the Python script:
```bash
python script.py
```

### **2. Main Interface**
- **Left Panel**: List of categories and subreddits with checkboxes.
- **Right Panel**: Displays the current image, its name, and size.

### **3. Select Subreddits**
- Select the desired subreddits by checking the boxes in the list.

### **4. Sort Images**
- Click the **"Sort images"** button to sort images into folders corresponding to the selected subreddits.

### **5. Change Source Folder**
- Use the **"Change source folder"** button to select a different folder containing images.

---

## **Generated Folder Structure**

When sorting images, a folder structure will be created under a `Content/` directory:
```
Content/
├── subreddit1/
│   ├── image1_[subreddit1]_date.jpg
│   └── image2_[subreddit1]_date.jpg
├── subreddit2/
│   └── image3_[subreddit2]_date.jpg
...
```

---

## **Customization**

### Modify Subreddit List
To update the categories and subreddits:
1. Open the `subreddit_list.txt` file.
2. Add or modify the existing lines:
   - Example format:
     ```
     [CATEGORY]Nature
     EarthPorn, 2000000, 500, Amazing landscapes
     ```

---

## **Credits**
Developed with professionalism and passion by **Sofian Lahlou**.