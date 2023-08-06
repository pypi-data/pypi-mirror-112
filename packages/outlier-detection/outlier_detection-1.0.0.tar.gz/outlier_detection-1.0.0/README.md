# Outlier Detection
Detect outliers from pandas dataframe using various statistical tools
# INSTALLATION AND USAGE
```python
!pip install outlier-detection
from outlier_detection import utils

# Pandas Dataframe
df

# Detect outliers using IQR Method
# On overall data
utils.detect_outliers_using_iqr(df, 'numeric_column_name')

# Based on factors data
utils.detect_outliers_using_iqr(df, 'numeric_column_name', is_factor=True, factor='categorical_column_name')
```