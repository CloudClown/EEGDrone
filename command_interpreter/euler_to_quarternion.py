#need variables yaw, pitch, roll from messages

q0=math.cos(roll/2)*math.cos(pitch/2)*math.cos(yaw/2)+math.sin(roll/2)*math.sin(pitch/2)*math.sin(yaw/2)
q1=math.sin(roll/2)*math.cos(pitch/2)*math.cos(yaw/2)-math.cos(roll/2)*math.sin(pitch/2)*math.sin(yaw/2)
q2=math.cos(roll/2)*math.sin(pitch/2)*math.cos(yaw/2)+math.sin(roll/2)*math.cos(pitch/2)*math.sin(yaw/2)
q3=math.cos(roll/2)*math.cos(pitch/2)*math.sin(yaw/2)-math.sin(roll/2)*math.sin(pitch/2)*math.cos(yaw/2)