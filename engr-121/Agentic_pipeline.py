from typing import List, Dict, Callable
import logging


class AgentAction:
    def __init__(self, name: str, function: Callable, description: str):
        self.name = name
        self.function = function
        self.description = description

class AgentPipeline:
    def __init__(self):
        self.available_actions: Dict[str, AgentAction] = {}
        self.action_history: List[Dict] = []
        
        # Register default actions
        self.register_default_actions()
        
    def register_action(self, name: str, function: Callable, description: str):
        """Register a new action the agent can perform"""
        self.available_actions[name] = AgentAction(name, function, description)
        
    def execute_action(self, action_name: str, **kwargs):
        """Execute a registered action"""
        if action_name in self.available_actions:
            action = self.available_actions[action_name]
            try:
                result = action.function(**kwargs)
                self.action_history.append({
                    'action': action_name,
                    'params': kwargs,
                    'success': True,
                    'result': result
                })
                logging.info(f"Action {action_name} executed with result: {result}")
                return result
            except Exception as e:
                logging.error(f"Error executing action {action_name}: {e}")
                self.action_history.append({
                    'action': action_name,
                    'params': kwargs,
                    'success': False,
                    'error': str(e)
                })
                return None
        else:
            logging.error(f"Action {action_name} not found")
            return None

    def alert(self, message: str):
        """Send an alert about thermal conditions"""
        logging.warning(f"THERMAL ALERT: {message}")
        return True

    def log_event(self, event_type: str, details: str):
        """Log a thermal system event"""
        logging.info(f"THERMAL EVENT - {event_type}: {details}")
        return True

    def register_default_actions(self):
        """Register the default set of actions"""
        self.register_action(
            "alert",
            self.alert,
            "Send alert about thermal conditions"
        )
        
        self.register_action(
            "log_event",
            self.log_event,
            "Log thermal system events"
        )
        
        self.register_action(
            "record_anomaly",
            lambda details: self.log_event("ANOMALY", details),
            "Record system anomalies"
        )
        
        self.register_action(
            "maintenance_alert",
            lambda msg: self.alert(f"MAINTENANCE NEEDED: {msg}"),
            "Alert about maintenance needs"
        )

# Initialize pipeline
pipeline = AgentPipeline() 