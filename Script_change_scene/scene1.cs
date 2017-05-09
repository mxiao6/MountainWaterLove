using UnityEngine;
using System.Collections;

public class Start : MonoBehaviour {
	private float endTime;
	public float duration;
	void Start() {
		endTime = Time.time + duration;
	}
	
	void Update () {
		if ( Time.time <= endTime ) {
			Application.LoadLevel("s2");
		}
	}
}
