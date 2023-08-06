import numpy as np

def nmf(X, rank, max_iter=7000, error_limit=1e-12,fit_error_limit=1e-12):
    '''
    Nonnegative matrix decomposition using Alternating Least Squares 

    X =A*Y

    '''

    eps = 1e-12
    mask = np.ones_like(X)
    rows, columns = np.shape(X)
    A =np.random.rand(rows, rank)
    A = np.maximum(A,eps)
    Y = np.linalg.lstsq(A,X,rcond=-1)[0]
    Y = np.maximum(Y,eps)
    masked_X = np.multiply(mask,X)
    X_est_prev = np.dot(A,Y)
    for i in range(1,max_iter+1):
            top=np.dot(masked_X,np.transpose(Y))
            bottom=(np.dot(np.multiply(mask,np.dot(A,Y)),np.transpose(Y)))+eps
            A=np.multiply(A,top/bottom)
            A=np.maximum(A, eps)
            top=np.dot(np.transpose(A),masked_X)
            bottom=np.dot(np.transpose(A),np.multiply(mask,np.dot(A,Y)))+eps
            Y=np.multiply(Y,top/bottom)
            Y=np.maximum(Y,eps)
            fit_residual =np.sqrt(np.sum(np.multiply(mask,(X_est_prev-np.dot(A,Y)))**2))
            curRes =np.linalg.norm(np.multiply(mask,(X-np.dot(A,Y))),ord='fro')           
            if (curRes<error_limit or fit_residual<fit_error_limit):
                    break
    return A, Y