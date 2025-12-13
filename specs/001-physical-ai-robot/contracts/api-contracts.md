# API Contracts: Physical AI & Humanoid Robotics

## Command Processing API

### POST /api/v1/commands
**Description**: Accept natural language commands as text or voice input

**Request**:
```json
{
  "text": "Go to the red box and pick it up",
  "type": "text",
  "user_id": "uuid-string"
}
```

**Response (201 Created)**:
```json
{
  "command_id": "uuid-string",
  "status": "accepted",
  "plan_id": "uuid-string"
}
```

### GET /api/v1/commands/{command_id}
**Description**: Get the status of a specific command

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "text": "Go to the red box and pick it up",
  "type": "text",
  "status": "completed",
  "timestamp": "2025-12-14T10:30:00Z",
  "plan_id": "uuid-string"
}
```

## Plan Management API

### GET /api/v1/plans/{plan_id}
**Description**: Get details of a specific plan

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "command_id": "uuid-string",
  "status": "executing",
  "actions": [
    {
      "id": "uuid-string",
      "type": "navigate",
      "parameters": {
        "target_position": {"x": 1.5, "y": 2.0, "z": 0.0}
      },
      "status": "completed"
    },
    {
      "id": "uuid-string",
      "type": "grasp",
      "parameters": {
        "object_id": "uuid-string"
      },
      "status": "pending"
    }
  ],
  "created_at": "2025-12-14T10:30:00Z",
  "completed_at": null
}
```

## Environment Management API

### GET /api/v1/environments
**Description**: List available simulation environments

**Response (200 OK)**:
```json
[
  {
    "id": "uuid-string",
    "name": "Simple Room",
    "description": "A basic room environment with a few objects",
    "world_file_path": "/simulation/worlds/simple_room.world"
  }
]
```

### GET /api/v1/environments/{env_id}
**Description**: Get details of a specific environment

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "name": "Simple Room",
  "description": "A basic room environment with a few objects",
  "world_file_path": "/simulation/worlds/simple_room.world",
  "objects": [
    {
      "id": "uuid-string",
      "name": "Red Box",
      "type": "box",
      "position": {"x": 1.0, "y": 1.5, "z": 0.0},
      "properties": {
        "color": "red",
        "size": "small"
      }
    }
  ]
}
```

## Robot Control API

### GET /api/v1/robots
**Description**: List available robots

**Response (200 OK)**:
```json
[
  {
    "id": "uuid-string",
    "name": "Humanoid Robot",
    "model_file_path": "/robot_models/humanoid.urdf",
    "current_position": {"x": 0.0, "y": 0.0, "z": 0.0},
    "current_orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
  }
]
```

### POST /api/v1/robots/{robot_id}/teleport
**Description**: Teleport robot to a new position (for simulation purposes)

**Request**:
```json
{
  "position": {"x": 5.0, "y": 3.0, "z": 0.0},
  "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
}
```

**Response (200 OK)**:
```json
{
  "status": "teleported",
  "new_position": {"x": 5.0, "y": 3.0, "z": 0.0}
}
```

## Simulation Control API

### POST /api/v1/simulation/start
**Description**: Start the simulation

**Response (200 OK)**:
```json
{
  "status": "started",
  "simulation_time": 0.0
}
```

### POST /api/v1/simulation/stop
**Description**: Stop the simulation

**Response (200 OK)**:
```json
{
  "status": "stopped",
  "final_simulation_time": 120.5
}
```

### GET /api/v1/simulation/status
**Description**: Get current simulation status

**Response (200 OK)**:
```json
{
  "running": true,
  "simulation_time": 65.3,
  "real_time_factor": 1.0
}
```