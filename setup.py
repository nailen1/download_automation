from setuptools import setup, find_packages

setup(
    name="download_automation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "pynput",
        "pandas",
        "tqdm",
        "opencv-python",
        "numpy",
        "mss",
        "psutil",
        "boto3", 
        "shining_pebbles",
        "aws_s3_controller",
    ],
    author="Your Name",
    author_email="juneyoungpaak@gmail.com",
    description="A package for automating downloads",
    long_description=open("README.md").read(),  # 파일 경로 수정
    long_description_content_type="text/markdown",
    url="https://github.com/nailen1/download_automation.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
