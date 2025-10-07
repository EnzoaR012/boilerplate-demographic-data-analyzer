import os
import pandas as pd


def calculate_demographic_data(print_data: bool = True):
    """
    Analyze demographic data from the 1994 Census dataset (adult.data.csv).

    Parameters
    ----------
    print_data : bool, optional
        If True, prints the analysis results. Defaults to True.

    Returns
    -------
    dict
        A dictionary containing the computed metrics ready for unit testing.
    """

    # Load data — the starter repo places the file at the project root.
    csv_path = "adult.data.csv"
    if not os.path.exists(csv_path):
        if print_data:
            print("[erro] Arquivo 'adult.data.csv' não encontrado no diretório atual.")
            print("Coloque o CSV na raiz do projeto ou ajuste o caminho em demographic_data_analyzer.py (variável csv_path).")
        return {}

    df = pd.read_csv(
        csv_path,
        header=0,
        sep=",",
        skipinitialspace=True,
    )

    if print_data:
        print(f"[ok] Dados carregados de {csv_path}: {len(df)} linhas.")

    # 1. How many people of each race are represented in this dataset?
    race_count = df["race"].value_counts()

    # 2. What is the average age of men?
    average_age_men = round(df.loc[df["sex"] == "Male", "age"].mean(), 1)

    # 3. What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df["education"] == "Bachelors").mean() * 100, 1)

    # 4 & 5. Percentage with/without advanced education (>50K)
    advanced = {"Bachelors", "Masters", "Doctorate"}
    higher_education = df[df["education"].isin(advanced)]
    lower_education = df[~df["education"].isin(advanced)]

    higher_education_rich = round((higher_education["salary"] == ">50K").mean() * 100, 1)
    lower_education_rich = round((lower_education["salary"] == ">50K").mean() * 100, 1)

    # 6. Minimum number of hours a person works per week
    min_work_hours = int(df["hours-per-week"].min())

    # 7. Percentage of the people who work the minimum number of hours per week and earn >50K
    min_workers = df[df["hours-per-week"] == min_work_hours]
    rich_percentage = round((min_workers["salary"] == ">50K").mean() * 100, 1)

    # 8. Country with the highest percentage of people that earn >50K
       
    country_rich_pct = (
        df.groupby("native-country")["salary"]
          .apply(lambda s: (s == ">50K").mean() * 100)
          .sort_values(ascending=False)
    )
    highest_earning_country = country_rich_pct.index[0]
    highest_earning_country_percentage = round(float(country_rich_pct.iloc[0]), 1)

    # 9. Most popular occupation for those who earn >50K in India
    top_IN_occupation = (
        df[(df["native-country"] == "India") & (df["salary"] == ">50K")]["occupation"].value_counts().idxmax()
        if ((df["native-country"] == "India") & (df["salary"] == ">50K")).any()
        else None
    )

    if print_data:
        print("Number of each race:")
        print(race_count)
        print(f"Average age of men: {average_age_men}")
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print(
            f"Country with highest percentage of >50K earners: {highest_earning_country} "
            f"({highest_earning_country_percentage}%)"
        )
        print(f"Top occupations in India for >50K: {top_IN_occupation}")

    # Prepare results dict for testing
    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation,
    }


if __name__ == "__main__":
    # Quick manual run
    calculate_demographic_data(print_data=True)
