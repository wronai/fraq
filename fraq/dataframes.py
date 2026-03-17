"""
DataFrame export for fraq - Polars, Pandas, Arrow integration.

Direct export to popular DataFrame libraries without manual conversion.

Example:
    import polars as pl
    from fraq import generate
    from fraq.dataframes import to_polars
    
    # Generate and convert in one step
    df = to_polars({
        'temperature': 'float:10-40',
        'sensor_id': 'str',
    }, count=10000)
    
    # Or with pandas
    from fraq.dataframes import to_pandas
    df = to_pandas({...}, count=1000)
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    try:
        import polars as pl
        import pandas as pd
        import pyarrow as pa
    except ImportError:
        pass


def to_polars(
    fields: Dict[str, str],
    count: int = 100,
    seed: Optional[int] = None,
) -> "pl.DataFrame":
    """Generate records and return as Polars DataFrame.
    
    Args:
        fields: Field specifications (same as generate())
        count: Number of records
        seed: Random seed
    
    Returns:
        Polars DataFrame
    
    Raises:
        ImportError: If polars is not installed
    
    Example:
        >>> df = to_polars({'temp': 'float:10-40', 'id': 'str'}, count=1000)
        >>> print(df.head())
    """
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "Polars not installed. Install with: pip install fraq[polars] or pip install polars"
        )
    
    from fraq import generate
    
    records = generate(fields, count=count, seed=seed)
    return pl.DataFrame(records)


def to_pandas(
    fields: Dict[str, str],
    count: int = 100,
    seed: Optional[int] = None,
) -> "pd.DataFrame":
    """Generate records and return as Pandas DataFrame.
    
    Args:
        fields: Field specifications (same as generate())
        count: Number of records
        seed: Random seed
    
    Returns:
        Pandas DataFrame
    
    Raises:
        ImportError: If pandas is not installed
    
    Example:
        >>> df = to_pandas({'temp': 'float:10-40', 'id': 'str'}, count=1000)
        >>> print(df.head())
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "Pandas not installed. Install with: pip install fraq[pandas] or pip install pandas"
        )
    
    from fraq import generate
    
    records = generate(fields, count=count, seed=seed)
    return pd.DataFrame(records)


def to_arrow(
    fields: Dict[str, str],
    count: int = 100,
    seed: Optional[int] = None,
) -> "pa.Table":
    """Generate records and return as PyArrow Table.
    
    Args:
        fields: Field specifications (same as generate())
        count: Number of records
        seed: Random seed
    
    Returns:
        PyArrow Table
    
    Raises:
        ImportError: If pyarrow is not installed
    
    Example:
        >>> table = to_arrow({'temp': 'float:10-40', 'id': 'str'}, count=1000)
        >>> print(table.schema)
    """
    try:
        import pyarrow as pa
    except ImportError:
        raise ImportError(
            "PyArrow not installed. Install with: pip install fraq[arrow] or pip install pyarrow"
        )
    
    from fraq import generate
    
    records = generate(fields, count=count, seed=seed)
    
    # Convert to PyArrow Table
    import pandas as pd
    df = pd.DataFrame(records)
    return pa.Table.from_pandas(df)


# Convenience aliases for generate() with output parameter
def generate_df(
    fields: Dict[str, str],
    count: int = 100,
    seed: Optional[int] = None,
    output: str = "polars",
) -> Any:
    """Generate records with specified output format.
    
    Args:
        fields: Field specifications
        count: Number of records
        seed: Random seed
        output: Output format - 'polars', 'pandas', 'arrow'
    
    Returns:
        DataFrame in specified format
    
    Example:
        >>> df = generate_df({...}, count=1000, output='polars')
        >>> df = generate_df({...}, count=1000, output='pandas')
    """
    if output == "polars":
        return to_polars(fields, count, seed)
    elif output == "pandas":
        return to_pandas(fields, count, seed)
    elif output == "arrow":
        return to_arrow(fields, count, seed)
    else:
        raise ValueError(f"Unknown output format: {output}. Use 'polars', 'pandas', or 'arrow'.")
