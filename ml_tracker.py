import gspread
from datetime import datetime
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 1. Strict Schema Enforcement
class TrainingRun(BaseModel):
    timestamp: str
    dataset: str
    iterations: int
    solver: str
    accuracy: float

def log_experiment_to_sheets():
    # 2. Connect to Cloud Infrastructure
    gc = gspread.service_account(filename='service_account.json')
    sh = gc.open("ML Experiment Tracker").sheet1
    
    if not sh.row_values(1):
        sh.append_row(["Timestamp", "Dataset", "Max Iterations", "Solver", "Accuracy"])

    # 3. Load Real Data & Train a Real Model
    print("🤖 Loading Iris Dataset and preparing training partitions...")
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # We will test different "max_iter" configurations to see how accuracy changes
    experiments = [
        {"max_iter": 10, "solver": "saga"},
        {"max_iter": 50, "solver": "saga"},
        {"max_iter": 100, "solver": "lbfgs"}
    ]

    for exp in experiments:
        # Train the actual model
        model = LogisticRegression(max_iter=exp["max_iter"], solver=exp["solver"])
        model.fit(X_train, y_train)
        real_accuracy = model.score(X_test, y_test)

        # Validate metrics via Pydantic
        clean_run = TrainingRun(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dataset="Iris Flower Dataset",
            iterations=exp["max_iter"],
            solver=exp["solver"],
            accuracy=round(real_accuracy, 4)
        )

        # Push verified production data to cloud ledger
        sh.append_row([
            clean_run.timestamp,
            clean_run.dataset,
            clean_run.iterations,
            clean_run.solver,
            clean_run.accuracy
        ])
        print(f"✅ Logged Run: Solver={clean_run.solver} | Accuracy={clean_run.accuracy:.2%}")

if __name__ == "__main__":
    log_experiment_to_sheets()