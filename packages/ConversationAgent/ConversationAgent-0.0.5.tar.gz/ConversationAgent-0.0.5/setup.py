from setuptools import setup
setup(
    name='ConversationAgent',
    version='0.0.5',
    description='ConversationAgent',
    author='Theta',
    license='MIT',
    packages=['ConversationAgent',
              'ConversationAgent/jieba_zh/',
              'ConversationAgent/jieba_zh/analyse/',
              'ConversationAgent/jieba_zh/finalseg/',
              'ConversationAgent/jieba_zh/posseg/'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.py"]
    },
    zip_safe=False
)