using UnityEngine;
using System.Collections;

public class Start : MonoBehaviour {

	void Update () {
		if (Input.GetButtonDown("Y")) {
			Application.LoadLevel("Scene Terrain");
		}
	}
}
