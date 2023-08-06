import os
import numpy as np
from pkg_resources import resource_filename

from pinocchio import neutral

from gym_jiminy.common.envs import WalkerJiminyEnv
from gym_jiminy.common.controllers import PDController
from gym_jiminy.common.pipeline import build_pipeline


# Parameters of neutral configuration
DEFAULT_SHOULDER_ANGLE = 0.15
DEFAULT_ELBOW_ANGLE = 0.4
DEFAULT_KNEE_ANGLE = 0.8

# Default simulation duration (:float [s])
SIMULATION_DURATION = 20.0
# Ratio between the High-level neural network PID target update and Low-level
# PID torque update (:int [NA])
HLC_TO_LLC_RATIO = 1
# Stepper update period (:float [s])
STEP_DT = 1.0e-3

# PID proportional gains (one per actuated joint)
PID_KP = np.array([
    # torso, head
    2000.0, 200.0,
    # left arm: [5, 6, 1 (ShZ), 2 (ShY), 3 (ElZ), 4 (ElY)]
    100.0, 100.0, 200.0, 2000.0, 200.0, 2000.0,
    # right arm: [5, 6, 1 (ShZ), 2 (ShY), 3 (ElZ), 4 (ElY)]
    100.0, 100.0, 200.0, 2000.0, 200.0, 2000.0,
    # left leg: [1, 2, 3 (HpY), 4 (KnY), 5 (AkY), 6 (AkX)]
    200.0, 200.0, 2000.0, 2000.0, 2000.0, 200.0,
    # right leg: [1, 2, 3 (HpY), 4 (KnY), 5 (AkY), 6 (AkX)]
    200.0, 200.0, 2000.0, 2000.0, 2000.0, 200.0])
# PID derivative gains (one per actuated joint)
PID_KD = np.array([
    # torso, head
    0.01, 0.01,
    # left arm: [5, 6, 1 (ShZ), 2 (ShY), 3 (ElZ), 4 (ElY)]
    0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
    # right arm: [5, 6, 1 (ShZ), 2 (ShY), 3 (ElZ), 4 (ElY)]
    0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
    # left leg: [1, 2, 3 (HpY), 4 (KnY), 5 (AkY), 6 (AkX)]
    0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
    # right leg: [1, 2, 3 (HpY), 4 (KnY), 5 (AkY), 6 (AkX)]
    0.01, 0.01, 0.01, 0.01, 0.01, 0.01])

# Reward weight for each individual component that can be optimized
REWARD_MIXTURE = {
    'direction': 0.0,
    'energy': 0.0,
    'done': 1.0
}
# Standard deviation ratio of each individual origin of randomness
STD_RATIO = {
    'model': 0.0,
    'ground': 0.0,
    'sensors': 0.0,
    'disturbance': 0.0,
}


class TalosJiminyEnv(WalkerJiminyEnv):
    def __init__(self, debug: bool = False, **kwargs):
        # Get the urdf and mesh paths
        data_root_dir = os.path.join(
            resource_filename('gym_jiminy.envs', 'data'),
            "bipedal_robots/talos")
        urdf_path = os.path.join(data_root_dir, "talos_full_v2.urdf")

        # Initialize the walker environment
        super().__init__(**{**dict(
            urdf_path=urdf_path,
            mesh_path=data_root_dir,
            simu_duration_max=SIMULATION_DURATION,
            step_dt=STEP_DT,
            reward_mixture=REWARD_MIXTURE,
            std_ratio=STD_RATIO,
            avoid_instable_collisions=True,
            debug=debug), **kwargs})

    def _neutral(self):
        def joint_position_idx(joint_name):
            joint_idx = self.robot.pinocchio_model.getJointId(joint_name)
            return self.robot.pinocchio_model.joints[joint_idx].idx_q

        qpos = neutral(self.robot.pinocchio_model)
        qpos[joint_position_idx('arm_left_2_joint')] = DEFAULT_SHOULDER_ANGLE
        qpos[joint_position_idx('arm_left_4_joint')] = -DEFAULT_ELBOW_ANGLE
        qpos[joint_position_idx('arm_right_2_joint')] = -DEFAULT_SHOULDER_ANGLE
        qpos[joint_position_idx('arm_right_4_joint')] = -DEFAULT_ELBOW_ANGLE
        for s in ['left', 'right']:
            qpos[joint_position_idx(
                f'leg_{s}_3_joint')] = -0.5 * DEFAULT_KNEE_ANGLE
            qpos[joint_position_idx(
                f'leg_{s}_4_joint')] = DEFAULT_KNEE_ANGLE
            qpos[joint_position_idx(
                f'leg_{s}_5_joint')] = -0.5 * DEFAULT_KNEE_ANGLE
        return qpos


TalosPDControlJiminyEnv = build_pipeline(**{
    'env_config': {
        'env_class': TalosJiminyEnv
    },
    'blocks_config': [{
        'block_class': PDController,
        'block_kwargs': {
            'update_ratio': HLC_TO_LLC_RATIO,
            'pid_kp': PID_KP,
            'pid_kd': PID_KD
        },
        'wrapper_kwargs': {
            'augment_observation': False
        }}
    ]
})
