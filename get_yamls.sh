NAMESPACE="airflow"

kubectl get all -n $NAMESPACE -o yaml > resources.yaml
kubectl get configmap -n $NAMESPACE -o yaml > configmaps.yaml
kubectl get secret -n $NAMESPACE -o yaml > secrets.yaml
kubectl get pv -n $NAMESPACE -o yaml > persistentvolumes.yaml
kubectl get pvc -n $NAMESPACE -o yaml > persistentvolumeclaims.yaml
kubectl get service -n $NAMESPACE -o yaml > services.yaml
kubectl get deployment -n $NAMESPACE -o yaml > deployments.yaml
kubectl get statefulset -n $NAMESPACE -o yaml > statefulsets.yaml

mv ./*.yaml ./yamls/
