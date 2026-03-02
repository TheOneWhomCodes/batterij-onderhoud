
# setup

## maken van een virtual environment:
  buys z'n notaties

## downloaden van nodige libraries:

Eerst ga in je virtual environment, en updaten we onze lijst van packages.
```
source apriltag_env/bin/activate
sudo apt update
```

Daarna install pip van python, pip is de standaard package manager van python.

```
sudo apt install python3-pip -y
```


 ### Libraries van de camera:
   - pupil-apriltags:
  Dit library is nodig om apriltags effectief te kunnen scannen.
  
  **stap 1)** Download cmake:

  ```
  sudo apt install cmake -y
  ```

  **stap 2)** Download nu de pupil-apriltags library:
  
  ```
  pip install pupil-apriltags
  ```

  - cv2:
  Dit library is nodig om onze camera in werking te laten brengen.

  **stap 1)** Download cv2:

  ```
  sudo apt install python3-opencv -y
  ```
    
  - Numpy:
  
  Dit library is nodig voor de cv2 zodat hij met die camera data kan werken en kan vertalen.

  **stap 1)** Download Numpy:

  ```
  pip install numpy
  ```

   
    
    

  
 
  

    
