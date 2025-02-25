import torch
import torch.nn as nn # Neural network
import torch.optim as optim # Optimizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler







# !!!                        IMPORTANT                          !!!
# =================================================================
# This is the first file you should run for training a model
# Do NOT run any of the other ML files until you've run this one
# =================================================================







df = pd.read_csv("processed_surface_data.csv")

X = df[['Peak_Accel', 'Mean_Accel', 'Impact_Duration']].values
y = df['Label'].values

scaler = StandardScaler()
X = scaler.fit_transform(X)

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a neural network
class SurfaceClassifier(nn.Module):
    def __init__(self):
        super(SurfaceClassifier, self).__init__()
        self.fc1 = nn.Linear(3, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x

# Initialize model, loss, and optimizer
model = SurfaceClassifier()
criterion = nn.BCELoss()  # Binary Cross-Entropy Loss
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Train the model
epochs = 50
for epoch in range(epochs):
    optimizer.zero_grad()
    y_pred = model(X_train)
    loss = criterion(y_pred, y_train)
    loss.backward()
    optimizer.step()

    if (epoch+1) % 10 == 0:
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}')

# Save trained model
torch.save(model.state_dict(), "surface_classifier.pth")
print("Model saved as surface_classifier.pth")