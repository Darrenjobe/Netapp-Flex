import json
import sys
import os
import glob
def main():
# Instantiate infra template
    infrapayload = {
        "name": "nr.tss.netAppIntegration",
        "protocol_version": "1",
        "integration_version": "1.0.0",
        "metrics": [],
        "events": [],
        "inventory": {}
        }

    filepath = sys.argv[1]
    instFiles = glob.glob("{}NetApp_Aggregates_netapp*.out".format(filepath))

# Gather Data for NetApp Aggregate Metrics
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'PercentageUsed' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Aggregates", "source_file" : inst, "Aggregate_Name" : aggName, "State" : aggState, "Percentage_Used" : p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'AggregateName' in ln:
		    k = ln.split(":")
                    aggName = k[1]
                if 'State' in ln:
                    s = ln.split(":")
                    aggState = s[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Disk Metrics
    instFiles = glob.glob("{}NetApp_Disks_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'AverageLatency' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Disks", "source_file" : inst, "Home_Node_Name" : homeNodeName, "Shelf" : shelf, "Disk_Name" : diskName, "Error_Count" : errorCount , "Average_Latency": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'HomeNodeName' in ln:
    		    h = ln.split(":")
                    homeNodeName = h[1]
                if 'Shelf' in ln:
    		    s = ln.split(":")
                    shelf = s[1]
                if 'DiskName' in ln:
    		    d = ln.split(":")
                    diskName = d[1]
                if 'ErrorCount' in ln:
    		    e = ln.split(":")
                    errorCount = e[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Fan Sensor Metrics
    instFiles = glob.glob("{}NetApp_Fan_Sensors_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'SensorState' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Fan_Sensors", "source_file" : inst, "SensorName" : sensorName, "NodeName" : nodeName, "SensorState": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'SensorName' in ln:
        	    s = ln.split(":")
                    sensorName = s[1]
                if 'NodeName' in ln:
    		    n = ln.split(":")
                    nodeName = n[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Ports Metrics
    instFiles = glob.glob("{}NetApp_Ports_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'LinkStatus' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Ports", "source_file" : inst, "NodeName" : nodeName, "PortName" : portName, "LinkStatus": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'NodeName' in ln:
            	    n = ln.split(":")
                    nodeName = n[1]
                if 'PortName' in ln:
    		    p = ln.split(":")
                    portName = p[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Voltage Sensor Metrics
    instFiles = glob.glob("{}NetApp_Voltage_Sensors_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'SensorState' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Voltage", "source_file" : inst, "SensorName" : sensorName, "NodeName" : nodeName, "SensorState": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'SensorName' in ln:
               	    n = ln.split(":")
                    sensorName = n[1]
                if 'NodeName' in ln:
    		    p = ln.split(":")
                    nodeName = p[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Volumes Metrics
    instFiles = glob.glob("{}NetApp_Volumes_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'FilesUsed' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Voltage", "source_file" : inst, "VserverName" : vserverName, "VolumeName" : volumeName,"VolumeState" : volumeState, "PercentageUsed" : percentageUsed, "FilesTotal" : filesTotal, "FilesUsed": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'VserverName' in ln:
                    v = ln.split(":")
                    vserverName = v[1]
                if 'VolumeName' in ln:
    		    vn = ln.split(":")
                    volumeName = vn[1]
                if 'VolumeState' in ln:
                    vs = ln.split(":")
                    volumeState = vs[1]
                if 'PercentageUsed' in ln:
    		    p = ln.split(":")
                    percentageUsed = p[1]
                if 'FilesTotal' in ln:
    		    f = ln.split(":")
                    filesTotal = f[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Thermal Sensor Metrics
    instFiles = glob.glob("{}NetApp_Thermal_Sensors_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'SensorState' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Thermal_Sensors", "source_file" : inst, "SensorName" : sensorName, "NodeName" : nodeName, "SensorState": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'SensorName' in ln:
                    n = ln.split(":")
                    sensorName = n[1]
                if 'NodeName' in ln:
    		    p = ln.split(":")
                    nodeName = p[1]
        inst = inst[:-5]
    #json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    #print(json_string)
# Gather Data for NetApp Snapmirrors Metrics
    instFiles = glob.glob("{}NetApp_Snapmirrors_netapp*.out".format(filepath))
    for inst in instFiles:
        with open(inst) as opInst:
            for ln in opInst:
                ln = ''.join(ln.split())
                if "--------" in ln:
                    continue
                if "totalRecords" in ln:
                    continue
                if ln == 'DONE':
                    continue
                if 'UnhealthyReason' in ln:
                    p = ln.split(":")
                    t_json = {"event_type" : "NetApp_Voltage", "source_file" : inst, "SourceVolume" : sourceVolume, "DestVolume" : destVolume,"IsHealthy" : isHealthy, "UnhealthyReason": p[1]}
                    infrapayload['metrics'].append(t_json)
                    t_json = {}
                    continue
                if 'SourceVolume' in ln:
                    s = ln.split(":")
                    sourceVolume = s[1]
                if 'DestVolume' in ln:
    		    d = ln.split(":")
                    destVolume = d[1]
                if 'IsHealthy' in ln:
                    i = ln.split(":")
                    isHealthy = i[1]
        inst = inst[:-5]
    json_string = json.dumps(infrapayload, separators=(',', ":")) # Compact JSON structure
    print(json_string)
if __name__ == '__main__':
    main()

