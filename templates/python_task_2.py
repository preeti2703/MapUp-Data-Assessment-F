import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    pivot_df1 = df1.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    
    distance_matrix = pivot_df1.add(pivot_df1.T, fill_value=0)

    for idx in distance_matrix.index:
        distance_matrix.loc[idx, idx] = 0
    
    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    upper_triangle = distance_matrix.where(
        np.triu(np.ones(distance_matrix.shape), k=1).astype(bool)
    )
        
    unrolled_df = (
        upper_triangle.stack().reset_index()
                      .rename(columns={'id_start': 'id_start', 'id_end': 'id_end', 0: 'distance'})
    )
        
    unrolled_df = unrolled_df.rename_axis(None, axis=1)

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    avg_distance = result_unrolled[result_unrolled['id_start'] == reference_value]['distance'].mean()

    threshold_lower = avg_distance - (0.1 * avg_distance)
    threshold_upper = avg_distance + (0.1 * avg_distance)

    within_threshold = distance_df[
        (result_unrolled['id_start'] != reference_value) &
        (result_unrolled['distance'] >= threshold_lower) &
        (result_unrolled['distance'] <= threshold_upper)
    ]['id_start'].unique()

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    for vehicle in rate_coefficients:
        df[vehicle] = df['distance'] * rate_coefficients[vehicle]

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
     weekday_ranges = [
        ('00:00:00', '10:00:00', 0.8),
        ('10:00:00', '18:00:00', 1.2),
        ('18:00:00', '23:59:59', 0.8)
    ]
    weekend_ranges = [('00:00:00', '23:59:59', 0.7)]
   
    for index, row in df1.iterrows():
        start_time = pd.to_datetime(row['start_time']).time()
        end_time = pd.to_datetime(row['end_time']).time()
       
        start_day = pd.to_datetime(row['startDay']).strftime('%A')
        end_day = pd.to_datetime(row['endDay']).strftime('%A')
       
        if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for start, end, factor in weekday_ranges:
                if pd.to_datetime(start_time) >= pd.to_datetime(start).time() and \
                   pd.to_datetime(end_time) <= pd.to_datetime(end).time():
                    break
        else:
            for start, end, factor in weekend_ranges:
                if pd.to_datetime(start_time) >= pd.to_datetime(start).time() and \
                   pd.to_datetime(end_time) <= pd.to_datetime(end).time():
                    break

    return df
