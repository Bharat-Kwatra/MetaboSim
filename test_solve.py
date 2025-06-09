import cobra
import warnings

# Ignore the numerous warnings from the SBML model
warnings.filterwarnings("ignore")

print("--- Running Minimal Solver Test (Local File Version) ---")
print("This script will load a trusted local model and try to solve it.")

# Define the path to the trusted model file you uploaded
model_path = "test_data/e_coli_core.xml.gz"

# 1. Load the E. coli core model from the local file
try:
    print(f"\nStep 1: Loading model from '{model_path}'...")
    model = cobra.io.read_sbml_model(model_path)
    print("   - Successfully loaded model.")
except Exception as e:
    print(f"   - FAILED: Could not read the local model file. Error: {e}")
    print("\nMake sure you have downloaded 'e_coli_core.xml.gz' and placed it in the 'test_data' directory.")
    exit()

# 2. Set up the environment for the model
print("\nStep 2: Setting up the simulation environment...")
try:
    model.reactions.EX_glc__D_e.lower_bound = -10
    model.reactions.EX_o2_e.lower_bound = -20
    model.objective = "BIOMASS_Ecoli_core_w_GAM"
    print("   - Set glucose uptake, oxygen uptake, and biomass objective.")
except Exception as e:
    print(f"   - FAILED: Could not set up the model's environment. Error: {e}")
    exit()

# 3. Run the optimization
print("\nStep 3: Attempting to solve the model...")
solution = model.optimize()

# 4. Print the final results
print("\n--- FINAL DIAGNOSIS ---")
print(f"Solver status: {solution.status}")
print(f"Objective value (growth rate): {solution.objective_value}")

if solution.status == 'optimal' and solution.objective_value > 0:
    print("\nSUCCESS! The model is solvable.")
    print("This proves your Python environment is working correctly, but the original 'ecoli_core_model.xml' file is faulty.")
    print("FIX: For your project, delete the old model file and use this newly downloaded one instead.")
else:
    print("\nFAILURE. The model is still infeasible.")
    print("This proves the problem is with your Python environment (cobrapy or the underlying solver).")
    print("FIX: You need to reinstall your dependencies, ideally in a fresh environment.")