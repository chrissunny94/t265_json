# Script to free the port
fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081
